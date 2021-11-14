from simulator import simulator
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_structural_hazards/'


def test_IA_RS_hazard():
    state = simulator.run(root + 'test_IA_RS_hazard/IA_RS_hazard.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_IA_RS_hazard/IA_RS_hazard.tt')
    print(tt_gold)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['R5'] == 20
    assert state.registers['R6'] == 50
    assert state.registers['R7'] == -40
    assert state.registers['R8'] == 40
    assert tt_gold == tt_test


def test_FPA_RS_hazard():
    state = simulator.run(root + 'test_FPA_RS_hazard/FPA_RS_hazard.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_FPA_RS_hazard/FPA_RS_hazard.tt')
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F21'] == 6.1
    assert state.registers['F22'] == 13.0
    assert state.registers['F23'] == 5.0
    assert state.registers['F24'] == -5.0
    assert state.registers['F25'] == 9.1
    assert tt_gold == tt_test


def test_FPM_RS_hazard():
    state = simulator.run(root + 'test_FPM_RS_hazard/FPM_RS_hazard.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_FPM_RS_hazard/FPM_RS_hazard.tt')
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F5'] == 3.0
    assert state.registers['F6'] == 12.5
    assert state.registers['F7'] == 10.0
    assert state.registers['F8'] == 3.75
    assert tt_gold == tt_test


def test_LSU_RS_hazard():
    state = simulator.run(root + 'test_LSU_RS_hazard/LSU_RS_hazard.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_LSU_RS_hazard/LSU_RS_hazard.tt')
    print(state.get_instruction_table())
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F1'] == 1.5
    assert state.registers['F2'] == 10.0
    assert state.registers['F3'] == -1.0
    assert state.memory[3] == 1.5
    assert tt_gold == tt_test
    
    
def test_ROB_hazard():
    state = simulator.run(root + 'test_ROB_hazard/ROB_hazard.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    tt_gold.load_from_file(root + 'test_ROB_hazard/ROB_hazard.tt')
    print(state.get_instruction_table())
    print(tt_test)
    assert list(state.RAT.values()) == list(state.RAT.keys())
    assert state.registers['F1'] == -2.0
    assert state.registers['F2'] == 2.5
    assert state.registers['F3'] == 5.0
    assert state.registers['R4'] == 12
    assert tt_gold == tt_test
