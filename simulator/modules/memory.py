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

    def next_ready_load(self):
        '''
        Get oldest RS that hasn't already gone to memory
        '''
        for rs in self.RS:
            if rs.instruction.type == 'LD' and rs.instruction.mem_cycle_start is None \
                and rs.is_complete():
                return rs
        return None

    def available_RS(self):
        return len(self.RS) < self.numRS

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
        if self.ALU_free and len(ready_rs) > 0:
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
            # rs.mem_alu_done = True #TODO: is this redundant? rs.is_complete() tells us this

            self.dealloc_instance()

    def check_memory_done(self, state):
        '''
        Check all LSQ entries if they are done in the memory stage.
        '''
        if self.memory_busy:
            for rs in self.RS:
                if state.clock_cycle == rs.instruction.mem_cycle_end:
                    memory_busy = False
                    if rs.instruction.type == 'LD':
                        load_val = state.memory[rs.mem_address]
                        rs.instruction.result = load_val
                    if rs.instruction.type == 'SD':
                        state.memory[rs.mem_address] = rs.op1_val

    def try_put_CDB(self, clock_cycle):
        if len(self.CDB_buffer) < self.CDB_capacity:
            for rs in self.RS:
                if clock_cycle >= rs.instrucion.mem_cycle_end:
                    self.CDB_buffer.append(rs.instruction)
                    self.RS.remove(rs)

    def store_forward(self, clock_cycle):
        for i, rs in enumerate(self.RS):
            # Look through whole LSQ for possible forwards
            if rs.instruction.type == 'SD' and self.rs_mem_is_ready(rs):
                for j, rs_target in enumerate(self.RS[i+1:]):
                    # Look at all subsequent instructions for loads
                    if rs_target.instruction.type == 'SD' and (not rs_target.is_complete() or \
                        rs_target.mem_address == rs.mem_address):
                        # Another store is going to forward or could potentially forward
                        break
                    if rs_target.instruction.type == 'LD' and rs_target.is_complete() \
                        and rs_target.mem_address == rs.mem_address and rs_target.instruction.result is None:
                        # This LD can be forwarded and it hasn't been forwarded yet
                        rs_target.instruction.result = rs.op1_val
                        rs_target.instruction.mem_cycle_start = clock_cycle
                        rs_target.instruction.mem_cycle_end = clock_cycle + 1

    def try_send_load(self, clock_cycle):
        next_load = self.next_ready_load()
        if not self.memory_busy and next_load is not None:
            next_load.instruction.mem_cycle_start = clock_cycle
            next_load.instruction.mem_cycle_end = clock_cycle + self.memCycles
            self.memory_busy = True

    def alloc_instance(self):
        self.ALU_free = False

    def dealloc_instance(self):
        set.ALU_free = True

    def calculate_result(self, rs):
        if rs.instruction.type == 'LD':
            return rs.op1_val + rs.instruction.offset
        if rs.instruction.type == 'SD':
            return rs.op2_val + rs.instruction.offset

    def read_CDB(self, inst):
        pass
