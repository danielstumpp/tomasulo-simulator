
import argparse

from .modules.timing_table import TimingTable

from .modules.state import State
from .modules.parsers import load_config

from .modules.fetch import fetch_instruction, FU_mapping
from .modules.func_units import initialize_units, RSEntry

from .modules.ROB import ROB


def issue_stage(state: State):
    '''
    1.1 Check for free reservation station
    1.2 Fill reservation station, remove instruction from queue (or increment PC)
    1.3 Search RAT for operands mapping and fetch available values
    1.4 Put instruction in ROB, updating RAT to point output register to ROB
    1.5 Increment PC if instruction was issued
    '''
    instruction = fetch_instruction(state)
    if not instruction:
        # PC is greater than length of instructions
        return False

    # Select the FU this instruction goes to
    FU = FU_mapping(state, instruction)

    if not FU.available_RS():
        return False

    if state.ROB.is_full():
        return False

    instruction.issue_cycle = state.clock_cycle
    rs_entry = RSEntry(instruction, FU.exCycles)

    # Look at RAT
    dest, op1, op2 = instruction.get_instruction_registers()
    if op1 is not None:
        rs_entry.op1_ptr = state.RAT[op1]
    if op2 is not None:
        rs_entry.op2_ptr = state.RAT[op2]

    # Fetch values that are ready
    if rs_entry.op1_ptr in state.registers.keys():
        rs_entry.op1_val = state.registers[rs_entry.op1_ptr]
        rs_entry.op1_ready = True
    elif 'ROB' in rs_entry.op1_ptr:
        # Check the ROB
        rob_idx = int(rs_entry.op1_ptr[3:])
        if state.ROB.entries[rob_idx].finished:
            rs_entry.op1_val = state.ROB.entries[rob_idx].instruction.result
            rs_entry.op1_ready = True

    if rs_entry.op2_ptr in state.registers.keys():
        rs_entry.op2_val = state.registers[rs_entry.op2_ptr]
        rs_entry.op2_ready = True
    elif 'ROB' in str(rs_entry.op2_ptr):
        # Check the ROB
        rob_idx = int(rs_entry.op2_ptr[3:])
        if state.ROB.entries[rob_idx].finished:
            rs_entry.op2_val = state.ROB.entries[rob_idx].instruction.result
            rs_entry.op2_ready = True

    # Put RS entry into RS array in FU
    FU.RS.append(rs_entry)

    # Put it in the ROB
    rob_idx = state.ROB.allocate_new(instruction)
    instruction.ROB_dest = rob_idx

    # Touch the RAT, points to ROB
    if dest is not None:
        state.RAT[dest] = f'ROB{rob_idx}'

    # Increment PC, change when we do branches
    state.PC += 1
    state.issued +=1
    return True


def execute_stage(state: State):
    '''
    1. Iterate over arithmetic FUs:
    1.1 If FU open and RS entry has ready operands, select oldest valid instructions
        and mark as executing in FU.
    2. Perform memory address computation for Load/Store instructions
        - Technically this is handled in EX but the memory_stage function will
        handle this computation for encapsulation purposes
    3. Handle instructions that finished executing this stage
    3.1 Mark that instruction is done
    3.2 Move instruction to locally buffered CDB queue (if there is space),
        clearing up RS station.
    '''

    for FU in [state.IA, state.FPA, state.FPM, state.LSU]:
        # Clear out completed values, free up reservation station, add to CDB buf
        FU.check_done(state.clock_cycle)

    for FU in [state.IA, state.FPA, state.FPM, state.LSU]:
        # Allocate instructions to instances
        FU.try_issue(state.clock_cycle)

    # TODO: Branches?


def memory_stage(state: State):
    '''
    1.0 Free up memory unit for instructions completing this cycle
    1.1 Push completed load instructions to local CDB buffer
    1.2 If you can, do store forwarding.
    1.3 Send memory instruction.
    '''
    # Free up the memory unit if the busy instruction finished this cycle
    state.LSU.check_memory_done(state)

    # Try to put finished loads on the CDB
    state.LSU.try_put_CDB(state.clock_cycle)

    # Do store-forwarding
    state.LSU.store_forward(state.clock_cycle)

    # Put loads in memory unit
    state.LSU.try_send_load(state.clock_cycle)


def writeback_stage(state: State):
    '''
    1. Iterate through all local CDB buffers. Pop oldest instruction.
    2. Put result in ROB and mark as ready
    3. Broadcast result to all waiting RS with this ROB entry operand
    '''
    # find the instruction waiting in CDB buffer the longest
    FPA_cycle = state.FPA.get_oldest_ready(state.clock_cycle)
    FPM_cycle = state.FPM.get_oldest_ready(state.clock_cycle)
    IA_cycle = state.IA.get_oldest_ready(state.clock_cycle)
    LSU_cycle = state.LSU.get_oldest_ready(state.clock_cycle)
    fu_cycles = [LSU_cycle, FPM_cycle, FPA_cycle, IA_cycle]
    # pop instruction to wb from the FU's CDB buffer
    FU_min_idx = fu_cycles.index(min(fu_cycles))
            
    if fu_cycles[FU_min_idx] != 2**32:
        if FU_min_idx == 0:
            wb_inst = state.LSU.pop_oldest_ready()
        elif FU_min_idx == 1:
            wb_inst = state.FPM.pop_oldest_ready()
        elif FU_min_idx == 2:
            wb_inst = state.FPA.pop_oldest_ready()
        elif FU_min_idx == 3:
            wb_inst = state.IA.pop_oldest_ready()
        else:
            assert False, 'should not be here'
    else:
        return  # no write backs happen on this cycle, nothing ready

    # effectuate the wb cycle
    wb_inst.writeback_cycle = state.clock_cycle

    # put the wb instruction in the rob and mark finished
    state.ROB.entries[wb_inst.ROB_dest].instruction = wb_inst
    state.ROB.entries[wb_inst.ROB_dest].finished = True

    # broadcast the wb result to RS
    for FU in [state.IA, state.FPA, state.FPM, state.LSU]:
        FU.read_CDB(wb_inst)


def commit_stage(state: State):
    '''
    1. Check head of ROB. If instruction is ready, update ARF.
    1.1. If RAT entry is same as ROB, reset RAT to ARF.
    1.2. Move ROB head. -> done in ROB.pop_head()
    1.3 Fire off exceptions.
    1.4 Update instruction metadata with timing, add to timing data structure
    '''
    # check if head of ROB is ready
    if state.ROB.head_ready():
        # head is ready to commit
        # pop the commit instruction from the ROB
        commit_inst = state.ROB.peak_head()
        if commit_inst.writeback_cycle < state.clock_cycle: # TODO, update for inst that don't wb
            # update the ARF
            dest, _, _ = commit_inst.get_instruction_registers()
            if dest is not None:
                state.registers[dest] = commit_inst.result

                # check if rat same as ROB
                if state.RAT[dest] == f'ROB{commit_inst.ROB_dest}':
                    state.RAT[dest] = dest

            # update timing
            commit_inst.commit_cycle = state.clock_cycle
            state.completed_instructions.append(commit_inst)
            state.committed += 1
            state.ROB.pop_head()
        else:
            return # the head just finished on this cycle, so don't commit
    else:
        if state.ROB.head_is_store():
            commit_inst = state.ROB.peak_head()
            # Store instruction at head, it is ready for memory unit
            lsq = state.LSU.RS[0]
            assert lsq.instruction.issue_cycle == commit_inst.issue_cycle, 'These should be the same instruction'

            if not state.LSU.memory_busy and state.LSU.rs_mem_is_ready(lsq, state.clock_cycle-1):
                state.LSU.memory_busy = True
                commit_inst.mem_cycle_start = state.clock_cycle
                commit_inst.mem_cycle_end = state.clock_cycle + (state.LSU.memCycles - 1)
                
                commit_inst.commit_cycle = state.clock_cycle
                state.completed_instructions.append(commit_inst)
                state.committed += 1
                state.ROB.pop_head()
        return  # still waiting for head to finish, no commits

    # TODO: Add `fire off exceptions' not sure what this was planned to be


def clock_tick(state: State):
    '''
    IF | EX | MEM | WB | COM
    '''
    # tick clock
    state.clock_cycle += 1

    good_issue = issue_stage(state)
    execute_stage(state)
    memory_stage(state)
    writeback_stage(state)
    commit_stage(state)

    # Check if program has finished
    if not good_issue and state.ROB.num_entries == 0 and state.issued == state.committed and not state.LSU.memory_busy:
        return False
    else:
        return True

def run(config_file):
    state = State()
    config_success = load_config(state, config_file)
    if not config_success:
        print('Config error. Exiting program')
        exit(0)

    initialize_units(state)

    print(state)
    while clock_tick(state):
        print(f'--------- Cycle {state.clock_cycle} ---------')
        #print(state.get_RAT_table())
        #print(state.get_ROB_table())
        #print(state.get_register_table())
        #print(state.get_RS_table())
        #input()
        

    return state
