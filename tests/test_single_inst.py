from simulator import simulator
from simulator.modules.state import State
from simulator.modules.timing_table import TimingTable


def test_addi_one_inst():
    state = simulator.run('tests/inputs/config/addi_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file('tests/inputs/timing/addi_single.tt')
    assert tt_gold == tt_test
    assert state.registers['R5'] == 100
    
