
import argparse
from simulator.modules.state import State
from simulator.modules.parsers import load_config

from simulator.modules.fetch import fetch_instruction, FU_mapping
from simulator.modules.func_units import initialize_units


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
        return False

    # Select the FU this instruction goes to
    FU = FU_mapping(state, instruction)



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
    pass



def memory_stage(state: State):
    '''
    1. See if you can send oldest instruction to memory
    1.1 If you can, do store forwarding.
    1.2 Push store-forwarded load instructions to local CDB buffer
    1.3 Send memory instruction, move head of queue.
    2. Handle ALU computation: calculate address for oldest instruction that has
        ready operands. Mark this as a cycle in the execute stage.
    '''
    pass


def writeback_stage(state: State):
    '''
    1. Iterate through all local CDB buffers. Pop oldest instruction.
    2. Put result in ROB and mark as ready
    3. Broadcast result to all waiting RS with this ROB entry operand
    '''
    pass


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
    while True:
        clock_tick(state)
