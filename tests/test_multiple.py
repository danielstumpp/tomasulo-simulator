from simulator.modules.maths import multiple, add


def test_multiple_3_4():
    assert multiple(3, 4) == 12


def test_add_3_4():
    assert add(3, 4) == 7

def test_add_4_4():
    assert add(4, 4) == 8

