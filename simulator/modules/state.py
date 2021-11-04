""" Defines the relevant objects for saving the state of the simulator"""

from typing import Dict

class State:
    """ Simulator State Object"""

    def __init__(self):
        """ Init Simulator State Object"""

        # initialize the system registers to zero
        register_keys = ["{}{}".format('R', i) for i in list(
            range(32))] + ["{}{}".format('F', j) for j in list(range(32))]
        self.registers = dict.fromkeys(register_keys, 0)

        # initialize the system memory to zero
        self.memory = [0.0] * 64

        # initialize instruction memory
        self.instructions = []

        self.PC = 0     # program counter

        self.FU_config = {}
        self.ROBentries = 0
        self.CDBbufferLength = 0

        self.clock_cycle = 0

        # TODO: Add more here as needed ...
        self.ROB = None

        self.IA = None
        self.FPA = None
        self.FPM = None
        self.LSU = None

        self.RAT = None


    def __str__(self):
        '''
        Print function
        '''
        pass
