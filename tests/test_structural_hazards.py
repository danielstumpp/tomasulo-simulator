from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_structural_hazards/'


def test_IA_RS_hazard():
    state = simulator.run(root + 'test_IA_RS_hazard/IA_RS_hazard.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_IA_RS_hazard/IA_RS_hazard.tt')
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R5'] == 20
    assert state.registers['R6'] == 50
    assert state.registers['R7'] == -40
    assert state.registers['R8'] == 40
    assert tt_gold == tt_test
