""" Defines the relevant objects for saving the state of the simulator"""

from prettytable import PrettyTable

from .instruction import Instruction

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
        self.CDBbufferLength = 0  # same for all FU

        self.clock_cycle = 0

        # TODO: Add more here as needed ...
        self.ROB = None

        self.IA = None
        self.FPA = None
        self.FPM = None
        self.LSU = None

        self.RAT = {rk: rk for rk in register_keys}
        
        # push all the completed instructions to this list
        self.completed_instructions = []
        
        self.issued = 0
        self.committed = 0

    def get_instruction_table(self) -> str:
        """Return string with table of instructions in state"""

        inst_table = PrettyTable(['#', 'Instruction', 'DONE'])
        for i in range(len(self.instructions)):
            if self.PC > i:
                done = 'X'
            else:
                done = ' '
            inst_table.add_row(
                ['I{}'.format(i), self.instructions[i].str.upper(), done])

        inst_table.align['Instruction'] = "l"
        return inst_table.get_string()

    def get_memory_table(self) -> str:
        """Return string with memory table of state memory"""
        mem_table = PrettyTable(
            ['Byte Address', 'Value', '', 'Byte Address ', 'Value '])
        for i in range(int(len(self.memory)/2)):
            mem_table.add_row(
                [str(4*i), '\033[94m {} \033[0m'.format(str(self.memory[i])), '',
                 str(4*(i + 32)), '\033[94m {} \033[0m'.format(str(self.memory[i + 32]))])

        return mem_table.get_string()

    def get_register_table(self) -> str:
        """Return string of register table for state"""

        reg_table = PrettyTable(
            ['Integer Reg', 'Value', '', 'Float Reg', 'Value '])
        for i in range(32):
            reg_table.add_row(
                ['R{}'.format(i), '\033[94m {} \033[0m'.format(str(int(self.registers['R{}'.format(i)]))), '',
                 'F{}'.format(i), '\033[94m {} \033[0m'.format(float(self.registers['F{}'.format(i)]))])

        return reg_table.get_string()

    def get_RAT_table(self) -> str:
        tbl = PrettyTable(['Arch Reg', 'Mapping ', '', 'Arch Reg ', 'Mapping'])
        for i in range(32):
            tbl.add_row(['R{}'.format(i), self.RAT['R{}'.format(i)], '',
                         'F{}'.format(i), self.RAT['F{}'.format(i)]])

        return tbl.get_string()

    def get_ROB_table(self) -> str:
        return self.ROB.__str__()

    def get_RS_table(self) -> str:
        output = 'Integer Adder RS\n'
        output += self.IA.__str__() + '\n\n'
        output += 'FP Adder RS\n'
        output += self.FPA.__str__() + '\n\n'
        output += 'FP Multiply RS\n'
        output += self.FPM.__str__() + '\n\n'
        return output

    def __str__(self):
        '''
        Print function
        '''

        # TODO: combine all relavent prints for massive print

        report = 'TODO'
        return report
