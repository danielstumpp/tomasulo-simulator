from simulator.modules.instruction import Instruction
import simulator.modules.parsers as psr
from simulator.modules.state import State
from simulator.modules.timing_table import TimingTable


def test_bad_config_filename():
    fn = "bad_file.yml"
    state = State()
    assert psr.load_config(state, fn) == False


def test_good_config_filename():
    fn = 'tests/inputs/config/test1_config.yml'
    state = State()
    assert psr.load_config(state, fn) == True


def test_bad_memory_filename():
    fn = 'tests/inputs/mem/non-existant-mem-file.mem'
    state = State()
    assert psr.init_memory(state, fn) == False


def test_out_of_range_address():
    fn = 'tests/inputs/mem/bad_out_of_range.mem'
    state = State()
    assert psr.init_memory(state, fn) == False


def test_non_numeric_entry():
    fn = 'tests/inputs/mem/bad_non_numeric.mem'
    state = State()
    assert psr.init_memory(state, fn) == False


def test_good_mem_init():
    fn = 'tests/inputs/mem/good_test.mem'
    state = State()
    assert psr.init_memory(state, fn) == True
    # looping through byte addresses
    for i in range(6):
        assert state.memory[i] == 1.5*(i+1)


def test_bad_register_filename():
    fn = 'tests/inputs/reg/bad-reg-filename.reg'
    state = State()
    assert psr.init_registers(state, fn) == False


def test_bad_register_name():
    fn = 'tests/inputs/reg/bad_invalid_name.reg'
    state = State()
    assert psr.init_registers(state, fn) == False


def test_bad_int_value():
    fn = 'tests/inputs/reg/bad_int_value.reg'
    state = State()
    assert psr.init_registers(state, fn) == False


def test_good_reg_inti():
    fn = 'tests/inputs/reg/good_test.reg'
    state = State()
    assert psr.init_registers(state, fn) == True
    assert state.registers['F1'] == 1.99
    assert state.registers['F31'] == 10.5
    assert state.registers['R1'] == 10
    assert state.registers['R31'] == 15

def test_validate_instruction_LD_SD():
    il = ['LD','F3',8,'R4']
    inst = Instruction()
    assert psr.validate_instruction(il,inst) == True
    il = ['LD', 8, 9, 'R3']
    assert psr.validate_instruction(il, inst) == False
    il = ['LD', 'F9', 9, 'R33']
    assert psr.validate_instruction(il, inst) == False
    il = ['SD', 8, 9, 'R33']
    assert psr.validate_instruction(il, inst) == False
    il = ['LD', 'F', 9, 'R3']
    assert psr.validate_instruction(il, inst) == False
    il = ['SD', 'F12',24, 'R1']
    assert psr.validate_instruction(il, inst) == True

def test_validate_instruction_BNE_BEQ():
    il = ['BEQ', 'F3', 'R4', 8]
    inst = Instruction()
    assert psr.validate_instruction(il, inst) == True
    il = ['BNE', 'F3', 'R4', 8]
    assert psr.validate_instruction(il, inst) == True
    il = ['BNE', 'F3', 'R4', 'R9']
    assert psr.validate_instruction(il, inst) == False
    il = ['BEQ', 'F3', 0, 8]
    assert psr.validate_instruction(il, inst) == False
    il = ['BNE', 'A3', 'R4', 8]
    assert psr.validate_instruction(il, inst) == False
    il = ['BEQ', 9, 'R4', 8]
    assert psr.validate_instruction(il, inst) == False

def test_parse_instructions_good():
    fn = 'tests/inputs/inst/inst1.asm'
    state = State()
    assert psr.parse_instructions(state, fn) == True
    assert len(state.instructions) == 3
    assert state.instructions[0].type == 'ADD.D'
    assert state.instructions[0].Fd == 'F1' 
    assert state.instructions[0].Fs == 'F2'
    assert state.instructions[0].Ft == 'F3'
    assert state.instructions[1].type == 'LD'
    assert state.instructions[1].Fa == 'F4'
    assert state.instructions[1].offset == 8
    assert state.instructions[1].Ra == 'R10'
    assert state.instructions[2].offset == -3
    assert state.instructions[2].type == 'BNE'
    

def test_good_config():
    fn = 'tests/inputs/config/test1_config.yml'
    state = State()
    assert psr.load_config(state,fn) == True
    