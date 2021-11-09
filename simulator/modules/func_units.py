from simulator.modules.state import State
from simulator.modules.ROB import ROB

class RSEntry:
    def __init__(self, instruction, ex_cycles):
        '''
        OP1 is first operand
        OP2 if second operand (or immediate)
        '''
        self.instruction = instruction

        self.ex_cycles = ex_cycles

        self.executing = False

        self.op1_ptr = None
        self.op2_ptr = None
        self.op1_val = None
        self.op2_val = None

        self.op1_ready = False
        self.op2_ready = False

        if instruction.immediate is not None:
            op2_val = instruction.immediate
            op2_ready = True

    def issue_to_ALU(self, clock_cycle):
        pass

    def is_complete(self, clock_cycle):
        return clock_cycle > self.instruction.execute_cycle_end

    def is_ready(self):
        return self.op1_ready and self.op2_ready

    def read_CDB(self, CDB):
        pass


class FunctionalUnit:
    def __init__(self, numRS, exCycles, instances):

        # TODO: Implement CDB buffers?

        self.numRS = numRS
        self.exCycles = exCycles
        self.instances = instances

        self.RS = [None]*numRS


    def available_RS(self):
        '''
        Return index of first available RS, None otherwise
        '''
        for i in range(self.numRS):
            if self.RS[i] is None:
                return i
        return None

    def execute_operation(self):
        '''
        Each FU implements this to do sub, add, mult etc.
        '''
        pass


def initialize_units(state: State):
    IA_conf = state.FU_config['IA']
    state.IA = FunctionalUnit(IA_conf['numRS'], IA_conf['exCycles'], IA_conf['instances'])
    FPA_conf = state.FU_config['FPA']
    state.FPA = FunctionalUnit(FPA_conf['numRS'], FPA_conf['exCycles'], FPA_conf['instances'])
    FPM_conf = state.FU_config['FPM']
    state.FPM = FunctionalUnit(FPM_conf['numRS'], FPM_conf['exCycles'], FPM_conf['instances'])

    # TODO: Initialize ROB and CDB buffers
    state.ROB = ROB(state.ROBentries)
