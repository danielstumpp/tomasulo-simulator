from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_report_tests/'


def test_straight_1():
    state = simulator.run(root + 'test_straight_1/straight_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_straight_1/straight_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert tt_gold == tt_test
    

def test_straight_dep_1():
    state = simulator.run(root + 'test_straight_dep_1/straight_dep_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_straight_dep_1/straight_dep_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert tt_gold == tt_test
    assert state.registers['R10'] == 10
    assert state.registers['R11'] == 20
    assert state.registers['F10'] == 30
    assert state.registers['F11'] == 50
    assert state.registers['R20'] == 11
    assert state.registers['R21'] == 1
    assert state.registers['F20'] == 20
    assert state.registers['F31'] == -30
    assert state.memory[4] == 1
    assert state.memory[5] == -30
    assert state.memory[3] == 40
    

def test_straight_forwarding_1():
    state = simulator.run(root + 'test_straight_forwarding_1/straight_forwarding_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_straight_forwarding_1/straight_forwarding_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert tt_gold == tt_test
