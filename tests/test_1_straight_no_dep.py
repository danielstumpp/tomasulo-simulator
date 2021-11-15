from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_1_straight_no_dep/'


""" def test_straight_1():
    state = simulator.run(root + 'test_straight_1/straight_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_straight_1/straight_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R5'] == 100
    assert state.registers['R6'] == 115
    assert tt_gold == tt_test """
