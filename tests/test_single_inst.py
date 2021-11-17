from simulator import simulator
from simulator.modules.state import State
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_single_inst/'

def test_addi_one_inst():
    state = simulator.run(root + 'test_addi_one_inst/addi_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_addi_one_inst/addi_single.tt')
    assert tt_gold == tt_test
    assert state.registers['R5'] == 100
    assert list(state.RAT.values()) == list(state.RAT.keys())
    

def test_add_one_inst():
    state = simulator.run(root + 'test_add_one_inst/add_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_add_one_inst/add_single.tt')
    assert tt_gold == tt_test
    assert state.registers['R3'] == 30
    assert list(state.RAT.values()) == list(state.RAT.keys())
    

def test_add_d_one_inst():
    state = simulator.run(root + 'test_add_d_one_inst/add_d_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_add_d_one_inst/add_d_single.tt')
    assert tt_gold == tt_test
    assert state.registers['F5'] == 6.5
    assert list(state.RAT.values()) == list(state.RAT.keys())


def test_sub_one_inst():
    state = simulator.run(root + 'test_sub_one_inst/sub_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_sub_one_inst/sub_single.tt')
    assert tt_gold == tt_test
    assert state.registers['R3'] == -10
    assert list(state.RAT.values()) == list(state.RAT.keys())


def test_sub_d_one_inst():
    state = simulator.run(root + 'test_sub_d_one_inst/sub_d_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_sub_d_one_inst/sub_d_single.tt')
    assert tt_gold == tt_test
    assert state.registers['F5'] == 2.5
    assert list(state.RAT.values()) == list(state.RAT.keys())
    

def test_mult_d_one_inst():
    state = simulator.run(root + 'test_mult_d_one_inst/mult_d_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_mult_d_one_inst/mult_d_single.tt')
    assert tt_gold == tt_test
    assert state.registers['F5'] == 9.0
    assert list(state.RAT.values()) == list(state.RAT.keys())


def test_ld_one_inst():
    state = simulator.run(root + 'test_ld_one_inst/ld_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_ld_one_inst/ld_single.tt')
    assert tt_gold == tt_test
    assert state.registers['F31'] == 3.4
    assert list(state.RAT.values()) == list(state.RAT.keys())


def test_sd_one_inst():
    state = simulator.run(root + 'test_sd_one_inst/sd_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_sd_one_inst/sd_single.tt')
    assert len(state.LSU.RS) == 0
    assert tt_gold == tt_test
    assert state.memory[4] == 4.5
    assert list(state.RAT.values()) == list(state.RAT.keys())


def test_nop_one_inst():
    state = simulator.run(root + 'test_nop_one_inst/nop_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_nop_one_inst/nop_single.tt')
    assert len(state.LSU.RS) == 0
    assert state.registers['R0'] == 0
    assert state.registers['R1'] == 10
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert tt_gold == tt_test
    
