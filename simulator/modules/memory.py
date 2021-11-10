class MemoryUnit:
    def __init__(self, numRS, exCycles, memCycles, instances, CDBbufferLength):
        self.numRS = numRS
        self.exCycles = exCycles
        self.memCycles = memCycles
        self.instances = instances

        self.RS = [] # The load/store queue

        self.CDB_capacity = CDBbufferLength
        self.CDB_buffer = []

        self.ALU_free = True

        self.memory_busy = False

    def next_mem_rs(self):
        '''
        Get oldest RS that hasn't already gone to memory
        '''
        for rs in self.RS:
            if rs.instruction.mem_cycle_start is None:
                return rs

    def available_RS(self):
        return len(self.ls_queue) < self.numRS

    def rs_mem_is_ready(self, rs):
        '''
        Is this RS ready to be sent to memory?
        This is done in memory stage
        '''
        if rs.instruction.type == 'LD':
            return rs.is_complete()
        if rs.intruction.type == 'SD':
            return rs.op1_ready and rs.is_complete()

    def rs_is_ready(self, rs):
        '''
        Is this reservation station ready for address/offset computation?
        This is done in execution stage
        '''
        if rs.instruction.type == 'LD':
            return rs.op1_ready and not rs.executing
        if rs.instruction.type == 'SD':
            return rs.op2_ready and not rs.executing

    def try_issue(self, clock_cycle):
        ready_rs = [rs_entry for rs_entry in self.RS if self.rs_is_ready(rs_entry)]
        ready_rs.sort(key=lambda x: x.issue_cycle)
        if ALU_free and len(ready_rs) > 0:
            rs = ready_rs[0]
            rs.executing = True
            rs.instruction.execute_cycle_start = clock_cycle
            rs.instruction.execute_cycle_end = clock_cycle + self.exCycles

            self.alloc_instance()

    def check_done(self, clock_cycle):
        # Check that ALU computation is done
        rs_complete = [rs for rs in self.RS if rs.is_complete()]
        rs_complete.sort(key=lambda x: x.issue_cycle)
        if len(rs_complete) > 0:
            rs = rs_complete[0]
            rs.mem_address = self.calculate_result(rs)
            rs.mem_alu_done = True

            self.dealloc_instance()

    def check_memory_done(self, state):
        if self.memory_busy:
            for rs in self.RS:
                if state.clock_cycle == rs.instruction.mem_cycle_end:
                    memory_busy = False
                    if rs.instruction.type == 'LD':
                        load_val = state.memory[rs.mem_address]
                        rs.instruction.result = load_val
                    if rs.instruction.type == 'SD':
                        state.memory[rs.mem_address] = rs.op1_val



    def alloc_instance(self):
        self.ALU_free = False

    def dealloc_instance(self):
        set.ALU_free = True

    def calculate_result(rs):
        if rs.instruction.type == 'LD':
            return rs.op1_val + rs.instruction.offset
        if rs.instruction.type == 'SD':
            return rs.op2_val + rs.instruction.offset
