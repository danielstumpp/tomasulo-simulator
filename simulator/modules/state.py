""" Defines the relevant objects for saving the state of the simulator"""

from typing import Dict
from prettytable import PrettyTable


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
        self.CDBbufferLength = 0 # same for all FU

        self.clock_cycle = 0

        # TODO: Add more here as needed ...
        self.ROB = None

        self.IA = None
        self.FPA = None
        self.FPM = None
        self.LSU = None

        self.RAT = {rk:rk for rk in register_keys}

    def __str__(self):
        '''
        Print function
        '''

        inst_table = PrettyTable(['#', 'Instruction', 'DONE'])
        for i in range(len(self.instructions)):
            if self.PC > i:
                done = 'X'
            else:
                done = ' '
            inst_table.add_row(
                ['I{}'.format(i), self.instructions[i].str.upper(),done])

        inst_table.align['Instruction'] = "l"
        inst_block = inst_table.get_string()

        mem_table = PrettyTable(
            ['Byte Address', 'Value', '', 'Byte Address ', 'Value '])
        for i in range(int(len(self.memory)/2)):
            mem_table.add_row(
                [str(4*i), '\033[94m {} \033[0m'.format(str(self.memory[i])), '',
                 str(4*(i + 32)), '\033[94m {} \033[0m'.format(str(self.memory[i + 32]))])

        reg_table = PrettyTable(
            ['Integer Reg', 'Value', '', 'Float Reg', 'Value '])
        for i in range(32):
            reg_table.add_row(
                ['R{}'.format(i), '\033[94m {} \033[0m'.format(str(int(self.registers['R{}'.format(i)]))), '',
                 'F{}'.format(i), '\033[94m {} \033[0m'.format(float(self.registers['F{}'.format(i)]))])


        data_report = PrettyTable([' ----- Register States -----', '----- Memory States -----'])
        data_report.add_row([reg_table.get_string(), mem_table.get_string()])

        report = data_report.get_string() + '\n' + inst_block
        return report
