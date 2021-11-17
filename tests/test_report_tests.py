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
    assert state.memory[1] == 5.5
    assert state.memory[2] == 2.75
    assert state.registers['F1'] == 5.5
    assert state.registers['F2'] == 2.75
    assert state.registers['F3'] == 2.75
    assert state.registers['F4'] == 2.75
    assert state.registers['F5'] == 2.75
    
    
def test_straight_hazards_1():
    state = simulator.run(root + 'test_straight_hazards_1/straight_hazards_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_straight_hazards_1/straight_hazards_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert tt_gold == tt_test
    assert state.registers['F1'] == 252.5
    assert state.registers['R1'] == 102
    assert state.registers['R2'] == 103
    assert state.registers['R10'] == 108
    assert state.registers['R11'] == 109
    assert state.registers['R3'] == 15
    assert state.registers['F5'] == 150
    assert state.registers['F10'] == 1.9
    assert state.registers['F15'] == -2.5
    assert state.memory[int(60/4)] == 108
    assert state.memory[int(56/4)] == 150
    

def test_straight_hazards_1():
    state = simulator.run(root + 'test_loop_hazards_1/loop_hazards_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_loop_hazards_1/loop_hazards_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    # assert tt_gold == tt_test
    assert state.registers['F1'] == 252.5
    assert state.registers['R1'] == 102
    assert state.registers['R2'] == 103
    assert state.registers['R10'] == 108
    assert state.registers['R11'] == 109
    assert state.registers['R3'] == 5
    assert state.registers['F5'] == 150
    assert state.registers['F10'] == 1.9
    assert state.registers['F15'] == -5
    assert state.memory[int(60/4)] == 108
    assert state.memory[int(56/4)] == 150
    assert state.memory[12//4] == 2


def test_simple_loop_1():
    state = simulator.run(root + 'test_simple_loop_1/simple_loop_1.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_simple_loop_1/simple_loop_1.tt')
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R2'] == 5
    assert state.registers['F4'] == 120
    assert state.registers['F5'] == sum(range(6))
    assert state.memory[0] == 120
    assert state.memory[1] == sum(range(6))
    #assert tt_gold == tt_test


def test_misprediction_exception():
    state = simulator.run(root + 'test_misprediction_exception/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_misprediction_exception/test.tt')
    assert tt_gold == tt_test
    assert state.memory[0] == 0
    assert state.memory[1] == 4

def test_robust_pred():
    state = simulator.run(root + 'test_robust_pred/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_robust_pred/test.tt')
    #assert tt_gold == tt_test
    assert state.registers['R1'] == 3
    assert state.registers['R3'] == 6
    assert state.registers['R4'] == 8
    assert state.registers['R5'] == 10
    assert list(state.RAT.values()) == list(state.RAT.keys())