class RSEntry:
    def __init__(self, intruction, clock_cycle, ex_cycles):
        self.instruction = instruction

        self.executing = False
        self.cycle_begin = None
        self.cycle_end = None

    def is_complete(self, clock_cycle):
        return clock_cycle >= cycle_end

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
        for i in range(numRS):
            if self.RS[i] is None:
                return i
        return None

    def execute_operation(self):
        '''
        Each FU implements this to do sub, add, mult etc.
        '''
        pass
