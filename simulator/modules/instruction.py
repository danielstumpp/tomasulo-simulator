""" Defines instruction class """

VALID_INSTRUCTIONS = ['LD', 'SD', 'BEQ', 'BNE',
                      'ADD', 'ADD.D', 'ADDI', 'SUB', 'SUB.D', 'MULT.D']


class Instruction:
    """ simulator instruction type """

    def __init__(self):
        self.Fa = None
        self.Fd = None
        self.Fs = None
        self.Ft = None
        self.Ra = None
        self.Rd = None
        self.Rs = None
        self.Rt = None
        self.immediate = None
        self.offset = None
        self.type = None
        self.str = None
        self.ID = None

        # Metadata
        self.issue_cycle = None
        self.execute_cycle_start = None
        self.execute_cycle_end = None
        self.mem_cycle_start = None
        self.mem_cycle_end = None
        self.writeback_cycle = None
        self.commit_cycle = None

        self.ROB_dest = None
        self.result = None


    def get_instruction_registers(self):
        '''
        return (Destination, Operand1, Operand2) tuple
        for any instruction.
        '''
        type = self.type
        if type in ['BEQ', 'BNE']:
            return None, self.Rs, self.Rt
        if type in ['ADD', 'SUB']:
            return self.Rd, self.Rs, self.Rt
        if type == 'ADDI':
            return self.Rs, self.Rt, None
        if type in ['ADD.D', 'SUB.D', 'MULT.D']:
            return self.Fd, self.Fs, self.Ft
        if type == 'SD':
            return None, self.Fa, self.Ra
        if type == 'LD':
            return self.Fa, self.Ra, None


    def __str__(self) -> str:
        return self.str
