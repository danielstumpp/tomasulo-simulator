from simulator import simulator
from simulator.modules.state import State
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_stalling_branch/'

def test_beq_taken():
    state = simulator.run(root + 'test_beq_taken/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_beq_taken/test.tt')
    assert tt_gold == tt_test
    assert state.registers['R1'] == 4
    assert list(state.RAT.values()) == list(state.RAT.keys())
    
def test_beq_not_taken():
    state = simulator.run(root + 'test_beq_not_taken/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_beq_not_taken/test.tt')
    assert tt_gold == tt_test
    assert state.registers['R1'] == 7
    assert list(state.RAT.values()) == list(state.RAT.keys())

def test_bne_taken():
    state = simulator.run(root + 'test_bne_taken/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_bne_taken/test.tt')
    assert tt_gold == tt_test
    assert state.registers['R1'] == 4
    assert list(state.RAT.values()) == list(state.RAT.keys())

def test_bne_not_taken():
    state = simulator.run(root + 'test_bne_not_taken/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_bne_not_taken/test.tt')
    assert tt_gold == tt_test
    assert state.registers['R1'] == 7
    assert list(state.RAT.values()) == list(state.RAT.keys())