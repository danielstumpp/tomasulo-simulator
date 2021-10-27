from simulator.modules import state

def test_state_mem_init():
    test_state = state.State()
    assert len(test_state.memory) == 64
    for i in range(len(test_state.memory)):
        assert test_state.memory[i] == 0


def test_state_reg_init():
    test_state = state.State()
    assert len(test_state.registers) == 32 * 2
    for k in test_state.registers.keys():
        assert test_state.registers[k] == 0
