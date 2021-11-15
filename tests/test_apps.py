from simulator import simulator
from simulator.modules.state import State
from simulator.modules.timing_table import TimingTable

root = 'tests/inputs/test_apps/'

def test_fib():
    '''
    memory[0]: argument for which fib number to calculate
    memory[1]: result returned by program
    '''
    state = simulator.run(root + 'test_fib/test.yml')
    tt_test = TimingTable()
    tt_gold = TimingTable()
    tt_test.load_from_state(state)
    # tt_gold.load_from_file(root + 'test_simple_loop/test.tt')
    # assert tt_gold == tt_test
    print(tt_test)
    print('fib result',state.memory[1])
    # print(state.memory)
    assert state.memory[1] == 233
    assert list(state.RAT.values()) == list(state.RAT.keys())
