
import argparse
from os import stat

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
    elif 'ROB' in rs_entry.op2_ptr:
        # Check the ROB
        rob_idx = int(rs_entry.op2_ptr[3:])
        if state.ROB.entries[rob_idx].finished:
            rs_entry.op2_val = state.ROB.entries[rob_idx].instruction.result
            rs_entry.op2_ready = True

    # Put RS entry into RS array in FU
    FU.RS.append(rs_entry)

    # Put it in the ROB
    rob_idx = state.ROB.allocate_new()
    instruction.ROB_dest = rob_idx

    # Touch the RAT, points to ROB
    if dest is not None:
        state.RAT[dest] = f'ROB{rob_idx}'

    # Increment PC, change when we do branches
    state.PC += 1


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
    1. See if you can send oldest instruction to memory
    1.1 If you can, do store forwarding.
    1.2 Push store-forwarded load instructions to local CDB buffer
    1.3 Send memory instruction, move head of queue.
    2. Handle ALU computation: calculate address for oldest instruction that has
        ready operands. Mark this as a cycle in the execute stage.
    '''
    # Free up the memory unit if the busy instruction finished this cycle
    state.LSU.check_memory_done(state)

    if not state.LSU.memory_busy and len(state.LSU.RS) > 0:
        rs = state.LSU.next_mem_rs()
        if rs is not None and state.LSU.rs_mem_is_ready(rs):
            # Stores only go to memory in the commit stage
            if rs.instruction.type == 'SD':
                if state.ROB.head_idx == rs.instruction.ROB_dest:
                    state.ROB.entries[state.ROB.head_idx].instruction = rs.instruction
                    # ROB head is this store instruction
                    state.LSU.memory_busy = True
                    rs.instruction.mem_cycle_start = state.clock_cycle
                    rs.instruction.mem_cycle_end = state.clock_cycle + state.LSU.memCycles

            state.LSU.memory_busy = True
            rs.instruction.mem_cycle_start = state.clock_cycle
            rs.instruction.mem_cycle_end = state.clock_cycle + state.LSU.memCycles


def writeback_stage(state: State):
    '''
    1. Iterate through all local CDB buffers. Pop oldest instruction.
    2. Put result in ROB and mark as ready
    3. Broadcast result to all waiting RS with this ROB entry operand
    '''
    # find the instruction waiting in CDB buffer the longest
    FPA_cycle = state.FPA.get_oldest_ready()
    FPM_cycle = state.FPM.get_oldest_ready()
    IA_cycle = state.IA.get_oldest_ready()
    
    if FPA_cycle is None and FPM_cycle is None and IA_cycle is None:
        return  # no write backs happen on this cycle, nothing ready
    
    # pop instruction to wb from the FU's CDB buffer
    if FPA_cycle < FPM_cycle and FPA_cycle < IA_cycle:
        wb_inst = state.FPA.pop_oldest_ready()
    elif FPM_cycle < FPA_cycle and FPM_cycle < IA_cycle:
        wb_inst = state.FPM.pop_oldest_ready()
    elif IA_cycle < FPA_cycle and IA_cycle < FPM_cycle:
        wb_inst = state.FPM.pop_oldest_ready()
    else:
        assert False, 'ERROR: should not get here'
        
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
    1.2. Move ROB head.
    1.3 Fire off exceptions.
    1.4 Update instruction metadata with timing, add to timing data structure
    '''
    pass


def clock_tick(state: State):
    '''
    IF | EX | MEM | WB | COM
    '''
    issue_stage(state)
    execute_stage(state)
    memory_stage(state)
    writeback_stage(state)
    commit_stage(state)

    # Check if program has finished


def run(config_file):
    state = State()
    config_success = load_config(state, config_file)
    if not config_success:
        print('Config error. Exiting program')
        exit(0)

    initialize_units(state)

    print(state)
    while True:  # TODO: Probably want some break condition here
        clock_tick(state)
