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
