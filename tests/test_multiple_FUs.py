from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_multiple_FUs/'


def test_multiple_FPA():
    state = simulator.run(root + 'test_multiple_FPA/multiple_FPA.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_multiple_FPA/multiple_FPA.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F1'] == 1
    assert state.registers['F2'] == 3
    assert state.registers['F3'] == 4
    assert state.registers['F4'] == 5
    assert state.registers['F5'] == 6
    assert tt_gold == tt_test


def test_multiple_FPM():
    state = simulator.run(root + 'test_multiple_FPM/multiple_FPM.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_multiple_FPM/multiple_FPM.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F1'] == 1
    assert state.registers['F2'] == 2
    assert state.registers['F3'] == 3
    assert state.registers['F4'] == 20
    assert state.registers['F5'] == 5
    assert tt_gold == tt_test
    
def test_multiple_IA():
    state = simulator.run(root + 'test_multiple_IA/multiple_IA.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_multiple_IA/multiple_IA.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R10'] == 1
    assert state.registers['R11'] == 3
    assert state.registers['R12'] == 4
    assert state.registers['R14'] == 10
    assert state.registers['R13'] == 5
    assert tt_gold == tt_test
    
