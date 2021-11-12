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
    assert list(state.RAT.values()) == list(state.RAT.keys())
    

def test_add_one_inst():
    state = simulator.run('tests/inputs/config/add_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file('tests/inputs/timing/add_single.tt')
    assert tt_gold == tt_test
    assert state.registers['R3'] == 30
    assert list(state.RAT.values()) == list(state.RAT.keys())


def test_sub_one_inst():
    state = simulator.run('tests/inputs/config/sub_single.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file('tests/inputs/timing/sub_single.tt')
    assert tt_gold == tt_test
    assert state.registers['R3'] == -10
    assert list(state.RAT.values()) == list(state.RAT.keys())
