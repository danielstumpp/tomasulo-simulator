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
        try:
            inst.offset = int(inst_list[2])
        except:
            return False
        inst.Ra = inst_list[3]
        if (type(inst.Ra) != str or type(inst.offset) != int or type(inst.Ra) != str):
            return False
        else:
            return check_valid_reg(inst.Ra) and check_valid_reg(inst.Fa)
    elif op == 'BNE' or op == 'BEQ':
        inst.Rs = inst_list[1]
        inst.Rt = inst_list[2]
        try:
            inst.offset = int(inst_list[3])
        except:
            return False
        if (type(inst.Rs) != str or type(inst.Rt) != str or type(inst.offset) != int):
            return False
        else:
            return check_valid_reg(inst.Rs) and check_valid_reg(inst.Rt)
    elif op == 'ADD' or op == 'SUB':
        inst.Rd = inst_list[1]
        inst.Rs = inst_list[2]
        inst.Rt = inst_list[3]
        if (type(inst.Rd) != str or type(inst.Rs) != str or type(inst.Rt) != str):
            return False
        else:
            return check_valid_reg(inst.Rd) and check_valid_reg(inst.Rs) and check_valid_reg(inst.Rt)
    elif op == 'ADD.D' or op == 'SUB.D' or op == 'MULT.D':
        inst.Fd = inst_list[1]
        inst.Fs = inst_list[2]
        inst.Ft = inst_list[3]
        if (type(inst.Fd) != str or type(inst.Fs) != str or type(inst.Ft) != str):
            return False
        else:
            return check_valid_reg(inst.Fd) and check_valid_reg(inst.Fs) and check_valid_reg(inst.Ft)
    elif op == 'ADDI':
        inst.Rt = inst_list[1]
        inst.Rs = inst_list[2]
        try:
            inst.immediate = int(inst_list[3])
        except:
            return False
        if (type(inst.Rt) != str or type(inst.Rs) != str or type(inst.immediate) != int):
            return False
        else:
            return check_valid_reg(inst.Rt) and check_valid_reg(inst.Rs)

    else:
        print('ERROR: unknown issue in `validate_instruction`')
        return False


def parse_instructions(state: State, asm_file: str):
    """ Parses the input assembly file and adds instructions to the state"""
    # read in asm file as csv
    try:
        csv_file = open(asm_file, newline='')
    except:
        print("ERROR: asm file -- " +
              asm_file + " -- could not be opened!")
        return False

    try:
        reader = csv.reader(csv_file, delimiter=',')
    except:
        print("ERROR: could not read asm file")
        return False

    reader_list = list(reader)
    for i in range(len(reader_list)):
        line = reader_list[i]
        if len(line) == 4:
            op = line[0].strip().upper()
            r1 = line[1].strip().upper()
            r2 = line[2].strip().upper()
            r3 = line[3].strip().upper()

            inst = Instruction()
            valid = validate_instruction([op, r1, r2, r3], inst)
            if valid:
                state.instructions.append(inst)
            else:
                print('ERROR: Invalid Instruction -> line ', i+1)
                return False
        else:
            op = line[0].strip().upper()
            r1 = line[1].strip().upper()
            os_Ra = line[2].strip().upper()
            offset = int(os_Ra[0:os_Ra.find('(')])
            ra = os_Ra[os_Ra.find('(')+1:os_Ra.find(')')]

            if op != 'SD' and op != 'LD':
                return False

            inst = Instruction()
            valid = validate_instruction([op, r1, offset, ra], inst)
            if valid:
                state.instructions.append(inst)
            else:
                print('ERROR: Invalid Instruction -> line ',i+1)
                return False
    return True

