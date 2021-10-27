import simulator.modules.parsers as psr
from simulator.modules.state import State


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
