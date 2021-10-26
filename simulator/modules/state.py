""" Defines the relevant objects for saving the state of the simulator"""


class State:
    """ Simulator State Object"""

    def __init__(self):
        """ Init Simulator State Object"""

        # initialize the system registers to zero
        register_keys = ["{}{}".format('R', i) for i in list(
            range(32))] + ["{}{}".format('F', j) for j in list(range(32))]
        self.registers = dict.fromkeys(register_keys, 0)

        # initialize the system memory to zero
        self.memory = [0] * 256

        # initialize instruction memory
        self.instructions = []

        self.PC = 0     # program counter

        # TODO: Add more here as needed ... 


