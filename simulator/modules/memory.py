from .instruction import Instruction


class MemoryUnit:
    def __init__(self, numRS, exCycles, memCycles, instances, CDBbufferLength):
        self.numRS = numRS
        self.exCycles = exCycles
        self.memCycles = memCycles
        self.instances = instances

        self.RS = []  # The load/store queue

        self.CDB_capacity = CDBbufferLength
        self.CDB_buffer = []

        self.ALU_free = True

        self.memory_busy = False
        self.memory_free_cycle = 0

    def next_ready_load(self, clock_cycle):
        '''
        Get oldest RS that hasn't already gone to memory
        '''
        seen_addresses = []
        for rs in self.RS:
            if rs.instruction.type == 'SD':
                if rs.mem_address is None:
                    # A store's memory address is unknown - might have conflict
                    return None
                else:
                    seen_addresses.append(rs.mem_address)
            if rs.instruction.type == 'LD' and rs.instruction.mem_cycle_start is None \
                    and rs.is_complete(clock_cycle) and rs.mem_address not in seen_addresses:
                # Found a load instruction with operands ready and there is no memory dependency on an
                # older store instruction.
                return rs
        return None

    def available_RS(self):
        return len(self.RS) < self.numRS

    def rs_mem_is_ready(self, rs, clock_cycle):
        '''
        Is this RS ready to be sent to memory?
        This is done in memory stage
        '''
        if rs.instruction.type == 'LD':
            return rs.is_complete(clock_cycle)
        if rs.instruction.type == 'SD':
            return rs.op1_ready and rs.is_complete(clock_cycle)

    def rs_is_ready(self, rs, clock_cycle):
        '''
        Is this reservation station ready for address/offset computation?
        This is done in execution stage
        '''
        if rs.instruction.type == 'LD':
            return clock_cycle > rs.instruction.issue_cycle and rs.op1_ready and not rs.executing
        if rs.instruction.type == 'SD':
            return clock_cycle > rs.instruction.issue_cycle and rs.op2_ready and not rs.executing

    def try_issue(self, clock_cycle):
        ready_rs = [rs_entry for rs_entry in self.RS if self.rs_is_ready(
            rs_entry, clock_cycle)]
        ready_rs.sort(key=lambda x: x.instruction.issue_cycle)
        if self.ALU_free and len(ready_rs) > 0:
            rs = ready_rs[0]
            rs.executing = True
            rs.instruction.execute_cycle_start = clock_cycle
            rs.instruction.execute_cycle_end = clock_cycle + (self.exCycles-1)

            self.alloc_instance()

    def check_done(self, state, _):
        # Check that ALU computation is done
        rs_complete = [rs for rs in self.RS if (rs.is_complete(state.clock_cycle) and rs.mem_address is None)]
        rs_complete.sort(key=lambda x: x.instruction.issue_cycle)
        if len(rs_complete) > 0:
            rs = rs_complete[0]
            rs.mem_address = int(self.calculate_result(rs))
            self.dealloc_instance()

    def check_memory_done(self, state):
        '''
        Check all LSQ entries if they are done in the memory stage.
        '''
        if self.memory_busy:
            for rs in self.RS:
                if rs.instruction.mem_cycle_end is not None and state.clock_cycle == rs.instruction.mem_cycle_end:
                    self.memory_busy = False
                    if rs.instruction.type == 'LD':
                        load_val = state.memory[rs.mem_address]
                        if 'R' in rs.instruction.Fa:
                            load_val = int(load_val)
                        rs.instruction.result = load_val
                        #print(load_val)
                    if rs.instruction.type == 'SD':
                        if 'R' in rs.instruction.Fa:
                            state.memory[rs.mem_address] = int(rs.op1_val)
                        else:
                            state.memory[rs.mem_address] = rs.op1_val
                        self.RS.remove(rs)

        if state.clock_cycle >= self.memory_free_cycle:
            self.memory_busy = False

    def try_put_CDB(self, clock_cycle):
        done_rs = [rs for rs in self.RS if rs.instruction.mem_cycle_end is not None and clock_cycle >= rs.instruction.mem_cycle_end]
        done_rs.sort(key=lambda x: x.instruction.issue_cycle)
        for rs in done_rs:
            if len(self.CDB_buffer) < self.CDB_capacity:
                    self.CDB_buffer.append(rs.instruction)
                    self.RS.remove(rs)

    def store_forward(self, clock_cycle):
        for i, rs in enumerate(self.RS):
            # Look through whole LSQ for possible forwards
            if rs.instruction.type == 'SD' and self.rs_mem_is_ready(rs, clock_cycle):
                for j, rs_target in enumerate(self.RS[i+1:]):
                    # Look at all subsequent instructions for loads
                    if rs_target.instruction.type == 'SD' and (not rs_target.is_complete(clock_cycle) or
                                                               rs_target.mem_address == rs.mem_address):
                        # Another store is going to forward or could potentially forward
                        break
                    if rs_target.instruction.type == 'LD' and rs_target.is_complete(clock_cycle) \
                            and rs_target.mem_address == rs.mem_address and rs_target.instruction.result is None:
                        # This LD can be forwarded and it hasn't been forwarded yet
                        rs_target.instruction.result = rs.op1_val
                        rs_target.instruction.mem_cycle_start = clock_cycle
                        rs_target.instruction.mem_cycle_end = clock_cycle

    def try_send_load(self, clock_cycle):
        next_load = self.next_ready_load(clock_cycle)
        if not self.memory_busy and next_load is not None and next_load.instruction.execute_cycle_end < clock_cycle:
            next_load.instruction.mem_cycle_start = clock_cycle
            next_load.instruction.mem_cycle_end = clock_cycle + (self.memCycles - 1)
            self.memory_busy = True
            self.memory_free_cycle = clock_cycle + self.memCycles

    def alloc_instance(self):
        self.ALU_free = False

    def dealloc_instance(self):
        self.ALU_free = True

    def calculate_result(self, rs):
        if rs.instruction.type == 'LD':
            #assert (rs.op1_val + rs.instruction.offset)/4 % 1 == 0, 'Address not word aligned'
            if (rs.op1_val + rs.instruction.offset)/4 % 1 != 0 or \
                rs.op1_val + rs.instruction.offset < 0 or rs.op1_val + rs.instruction.offset > 255:
                rs.instruction.fault = True
                return 0
            return (rs.op1_val + rs.instruction.offset)//4
        if rs.instruction.type == 'SD':
            #assert (rs.op2_val + rs.instruction.offset)/4 % 1 == 0, 'Address not word aligned'
            if (rs.op2_val + rs.instruction.offset)/4 % 1 != 0 or\
                rs.op2_val + rs.instruction.offset < 0 or rs.op2_val + rs.instruction.offset > 255:
                rs.instruction.fault = True
                return 0
            return (rs.op2_val + rs.instruction.offset)//4

    def get_oldest_ready(self, clock_cycle):
        if len(self.CDB_buffer) > 0:
            if self.CDB_buffer[0].mem_cycle_end < clock_cycle:
                return self.CDB_buffer[0].mem_cycle_end
            else:
                return 2**32
        else:
            return 2**32  # TODO: probably a better way

    def pop_oldest_ready(self) -> Instruction:
        return self.CDB_buffer.pop(0)

    def read_CDB(self, CDB_inst: Instruction):
        """transmit cdb value to all of the FU reservation stations"""
        for rs in self.RS:
            rs.read_CDB(CDB_inst)
