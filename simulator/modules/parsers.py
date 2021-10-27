""" parser functions to convert input configurations into runnable simulator input"""
from simulator.modules.state import State
from simulator.modules.instruction import Instruction
from simulator.modules.instruction import VALID_INSTRUCTIONS
import yaml
import csv


def load_config(state: State, config_file: str):
    """ Loads the specified yaml configuration file and returns loaded initial state by ref"""
    # open yaml file
    try:
        yaml_file = open(config_file)
    except:
        print("ERROR: config file -- " +
              config_file + " -- could not be opened!")
        return False

    try:
        config = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        print("Error in configuration file:", exc)
        return False

    # TODO

    return True


def init_memory(state: State, mem_file: str):
    """ Initializes the memory of the state based on the provided memory file"""
    # read in memory file as csv
    try:
        csv_file = open(mem_file, newline='')
    except:
        print("ERROR: memory file -- " +
              mem_file + " -- could not be opened!")
        return False

    try:
        reader = csv.reader(csv_file, delimiter=',')
    except:
        print("ERROR: could not read mem file")
        return False

    reader_list = list(reader)
    for i in range(len(reader_list)):
        line = reader_list[i]

        # ensure inputs are numeric
        try:
            float(line[0].strip())
            float(line[1].strip())
        except:
            print("ERROR: Non-numeric memory entry -> line ", i + 1)
            return False

        addr = int(line[0].strip())
        val = float(line[1].strip())

        if addr < 256 and addr >= 0 and addr % 4 == 0:
            state.memory[int(addr/4)] = val
        else:
            print("ERROR: Invalid memory entry -> line ", i + 1)
            return False

    return True


def init_registers(state: State, reg_file: str):
    """ Initializes the registers of the state based on provided register value file"""
    # read in register file as csv
    try:
        csv_file = open(reg_file, newline='')
    except:
        print("ERROR: register file -- " +
              reg_file + " -- could not be opened!")
        return False

    try:
        reader = csv.reader(csv_file, delimiter=',')
    except:
        print("ERROR: could not read reg file")
        return False

    reader_list = list(reader)
    for i in range(len(reader_list)):
        line = reader_list[i]

        # check if string is valid register name
        if line[0].strip() not in state.registers:
            print('ERROR: Invalid register name -> line ', i + 1)
            return False
        # check if value is numeric
        try:
            float(line[1].strip())
        except:
            print('ERROR: Invalid register value -> line ', i + 1)
            return False

        reg = line[0].strip()
        val = float(line[1].strip())

        # check for floats put in int registers
        if val % 1 != 0 and reg[0] == 'R':
            print('ERROR: Float in Int Register -> line ', i + 1)
            return False
        else:
            # everything is good, put into register
            state.registers[reg] = val

    return True

def check_valid_reg(reg: str):
    state = State()
    return (reg in state.registers)

def validate_instruction(inst_list: list, inst: Instruction) -> bool:
    """ Validates a single instruction passed in as a list in the format [OP, R1, R2/Offset, R3/immediate"""
    op = str(inst_list[0]).strip().upper()
    if op not in VALID_INSTRUCTIONS:
        print('here')
        return False

    inst.type = op
    if op == 'LD' or op == 'SD':
        inst.Fa = inst_list[1]
        inst.offset = inst_list[2]
        inst.Ra = inst_list[3]
        if (type(inst.Ra) != str or type(inst.offset) != int or type(inst.Ra) != str):
            return False
        else:
            return check_valid_reg(inst.Ra) and check_valid_reg(inst.Fa)
    elif op == 'BNE' or op == 'BEQ':
        inst.Rs = inst_list[1]
        inst.Rt = inst_list[2]
        inst.offset = inst_list[3]
    elif op == 'ADD' or op == 'SUB':
        inst.Rd = inst_list[1]
        inst.Rs = inst_list[2]
        inst.Rt = inst_list[3]
    elif op == 'ADD.D' or op == 'SUB.D' or op == 'MULT.D':
        inst.Fd = inst_list[1]
        inst.Fs = inst_list[2]
        inst.Ft = inst_list[3]
    else:
        print('ERROR: unknown issue in `validate_instruction`')
        return False
    return True


def parse_instructions(state: State, asm_file: str):
    """ Parses the input assembly file and adds instructions to the state"""
    pass
