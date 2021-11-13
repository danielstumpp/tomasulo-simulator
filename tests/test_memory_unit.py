from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_memory_unit/'

def test_store_forward():
    state = simulator.run(root + 'test_store_forward/store_forward.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_store_forward/store_forward.tt')
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F2'] == 6.5
    assert state.memory[4] == 6.5
    assert tt_gold == tt_test


