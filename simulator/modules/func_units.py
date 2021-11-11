from .instruction import Instruction
from .state import State
from .ROB import ROB
from .memory import MemoryUnit

from prettytable import PrettyTable


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

        self.mem_alu_done = False
        self.mem_address = None

    def issue_to_ALU(self, clock_cycle):
        '''
        TODO decrement free_instances on issue, increment on complete
        '''
        pass

    def is_complete(self, clock_cycle):
        return clock_cycle >= self.instruction.execute_cycle_end

    def is_ready(self):
        return self.op1_ready and self.op2_ready and not self.executing

    def read_CDB(self, CDB_inst: Instruction):
        """Accepts CDB broadcast instruction and updates values if possible"""
        if CDB_inst.ROB_dest == self.op1_ptr:
            self.op1_val = CDB_inst.result
            self.op1_ready = True
        if CDB_inst.ROB_dest == self.op2_ptr:
            self.op2_val = CDB_inst.result
            self.op2_ready = True


class FunctionalUnit:
    def __init__(self, numRS, exCycles, instances, CDBbufferLength):

        # TODO: Implement CDB buffers?

        self.numRS = numRS
        self.exCycles = exCycles
        self.instances = instances
        self.free_instances = instances

        self.RS = []

        self.CDB_capacity = CDBbufferLength
        self.CDB_buffer = []

    def __str__(self) -> str:
        """ print functional unit table """
        tbl = PrettyTable(['Op', 'Dest-Tag', 'Tag1', 'Tag2', 'Val1', 'Val2'])

        for rs in self.RS:
            tbl.add_row([rs.instruction.str, 'ROB{}'.format(rs.instruction.ROB_dest), 
            str(rs.op1_ptr), str(rs.op2_ptr), str(rs.op1_val), str(rs.op2_val)])

        return tbl.get_string()

    def available_RS(self):
        '''
        Return index of first available RS, None otherwise
        '''
        return len(self.RS) < self.numRS

    def execute_operation(self):
        '''
        Each FU implements this to do sub, add, mult etc.
        '''
        pass

    def is_available(self):
        '''
        Can a RS entry start executing?
        '''
        pass

    def try_issue(self, clock_cycle):
        ready_rs = [rs_entry for rs_entry in self.RS if rs_entry.is_ready()]
        ready_rs.sort(key=lambda x: x.issue_cycle)
        for free_idx in range(min(self.free_instances, len(ready_rs))):
            rs = ready_rs[free_idx]
            rs.executing = True
            rs.instruction.execute_cycle_start = clock_cycle
            rs.instruction.execute_cycle_end = clock_cycle + self.exCycles

            self.alloc_instance()

    def check_done(self, clock_cycle):
        rs_complete = [rs for rs in self.RS if rs.is_complete()]
        rs_complete.sort(key=lambda x: x.issue_cycle)
        for rs in rs_complete:
            if len(self.CDB_buffer) < self.CDB_capacity:
                rs.instrucion.result = self.calculate_result(rs)

                self.CDB_buffer.append(rs.instruction)
                self.RS.remove(rs)

                self.dealloc_instance()
                
    def get_oldest_ready(self):
        return self.CDB_buffer[0].execute_cycle_end
    
    def pop_oldest_ready(self) -> Instruction:
        return self.CDB_buffer.pop(0)

    def read_CDB(self, CDB_inst: Instruction):
        """transmit cdb value to all of the FU reservation stations"""
        # TODO

    def alloc_instance(self):
        # To be overwritten by integer ALU
        pass

    def dealloc_instance(self):
        pass

    def calculate_result(self, rs_entry):
        itype = rs_entry.instruction.type
        if itype in ['ADD', 'ADDI', 'ADD.D']:
            res = rs_entry.op1_val + rs_entry.op2_val
        elif itype in ['SUB', 'SUB.D']:
            res = rs_entry.op1_val - rs_entry.op2_val
        elif itype in ['MULT.D']:
            res = rs_entry.op1_val * rs_entry.op2_val
        else:
            assert False
        return res


class IntegerUnit(FunctionalUnit):
    def __init__(self, numRS, exCycles, instances, CDBbufferLength):
        super().__init__(numRS, exCycles, instances, CDBbufferLength)

    def alloc_instance(self):
        self.free_instances -= 1
        assert self.free_instances >= 0

    def dealloc_instance(self):
        self.free_instances += 1
        assert self.free_instances <= self.instances


def initialize_units(state: State):
    IA_conf = state.FU_config['IA']
    state.IA = IntegerUnit(
        IA_conf['numRS'], IA_conf['exCycles'], IA_conf['instances'], state.CDBbufferLength)
    FPA_conf = state.FU_config['FPA']
    state.FPA = FunctionalUnit(
        FPA_conf['numRS'], FPA_conf['exCycles'], FPA_conf['instances'], state.CDBbufferLength)
    FPM_conf = state.FU_config['FPM']
    state.FPM = FunctionalUnit(
        FPM_conf['numRS'], FPM_conf['exCycles'], FPM_conf['instances'], state.CDBbufferLength)
    LSU_conf = state.FU_config['LSU']
    state.LSU = MemoryUnit(LSU_conf['numRS'], LSU_conf['exCycles'],
                           LSU_conf['memCycles'], LSU_conf['instances'], state.CDBbufferLength)

    state.ROB = ROB(state.ROBentries)
