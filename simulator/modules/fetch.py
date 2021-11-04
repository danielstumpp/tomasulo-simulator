from simulator.modules.state import State
from simulator.modules.instruction import Instruction

def fetch_instruction(state: State):
    assert state.PC > 0, 'PC value is negative and invalid.'
    if state.PC >= len(state.instructions):
        print('PC is greater than length of instruction stream. Program ended.')
        return False

    instruction = state.instructions[state.PC]
    return instruction

def FU_mapping(state: State, instruction: Instruction):
    type = instruction.type
    if type in ['ADD', 'SUB', 'ADDI', 'BEQ', 'BNE']:
        return state.IA
    if type in ['ADD.D, SUB.D']:
        return state.FPA
    if type in ['MULT.D']:
        return state.FPM
    assert False, 'that instruction type is not implemeted'
