from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_dep_inst/'

def test_addi_dep_inst():
    state = simulator.run(root + 'test_addi_dep_inst/addi_dep.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_addi_dep_inst/addi_dep.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R5'] == 100
    assert state.registers['R6'] == 115
    assert tt_gold == tt_test
    
    
def test_mult_d_dep_inst():
    state = simulator.run(root + 'test_mult_d_dep_inst/mult_d_dep.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_mult_d_dep_inst/mult_d_dep.tt')
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F10'] == 9.0
    assert state.registers['F1'] == 81.0
    assert tt_gold == tt_test


def test_R0_false_dep():
    state = simulator.run(root + 'test_R0_false_dep/R0_false_dep.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_R0_false_dep/R0_false_dep.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R0'] == 0
    assert state.registers['F1'] == 25
    assert state.registers['R1'] == 4
    assert tt_gold == tt_test

