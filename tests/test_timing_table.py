from simulator.modules.timing_table import TimingTable
from simulator.modules.state import State
import simulator.modules.parsers as psr

def test_good_timing_table_comparison():
    fn = 'tests/inputs/config/test1_config.yml'
    state = State()
    assert psr.load_config(state, fn) == True
    tt1 = TimingTable()
    tt1.load_from_state(state)
    tt2 = TimingTable()
    tt2.load_from_state(state)
    assert tt1 == tt2


def test_bad_timing_table_comparison():
    fn = 'tests/inputs/config/test1_config.yml'
    state = State()
    assert psr.load_config(state, fn) == True
    tt1 = TimingTable()
    tt1.load_from_state(state)
    tt2 = TimingTable()
    state.instructions[1].mem_cycle = 2
    tt2.load_from_state(state)
    assert tt1 != tt2


def test_dummy_csv_tt_good():
    ttfn = 'tests/inputs/timing/dummy1.tt'
    configfn = 'tests/inputs/config/test1_config.yml'
    state = State()
    psr.load_config(state, configfn)
    tt1 = TimingTable()
    tt1.load_from_state(state)
    tt2 = TimingTable()
    tt2.load_from_file(ttfn)
    assert tt1 == tt2


def test_dummy_csv_tt_wrong():
    ttfn = 'tests/inputs/timing/dummy2.tt'
    configfn = 'tests/inputs/config/test1_config.yml'
    state = State()
    psr.load_config(state, configfn)
    tt1 = TimingTable()
    tt1.load_from_state(state)
    tt2 = TimingTable()
    tt2.load_from_file(ttfn)
    assert tt1 != tt2

