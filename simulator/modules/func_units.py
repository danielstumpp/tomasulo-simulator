from modules.state import State

class RSEntry:
    def __init__(self, instruction, clock_cycle, ex_cycles):
        self.instruction = instruction

        self.executing = False
        self.cycle_begin = None
        self.cycle_end = None

    def is_complete(self, clock_cycle):
        return clock_cycle >= self.cycle_end

    def is_ready(self):
        pass

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
