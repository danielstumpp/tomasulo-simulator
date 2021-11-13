from simulator import simulator
from simulator.modules.timing_table import TimingTable

def test_addi_dep_inst():
    state = simulator.run('tests/inputs/config/addi_dep.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file('tests/inputs/timing/addi_dep.tt')
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R5'] == 100
    assert state.registers['R6'] == 115
    assert tt_gold == tt_test
    
