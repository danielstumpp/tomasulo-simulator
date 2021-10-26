import simulator.modules.parsers as psr
from simulator.modules.state import State

def test_bad_config_filename():
    fn = "bad_file.yml"
    state = State()
    assert psr.load_config(state, fn) == False

def test_good_config_filename():
    fn = 'tests/inputs/config/test1_config.yml'
    state = State()
    assert psr.load_config(state, fn) == True


