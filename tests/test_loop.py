from simulator import simulator
from simulator.modules.state import State
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_loop/'

def test_simple_loop():
    state = simulator.run(root + 'test_simple_loop/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_simple_loop/test.tt')
    assert tt_gold == tt_test
    assert state.registers['R1'] == 5
    assert list(state.RAT.values()) == list(state.RAT.keys())
