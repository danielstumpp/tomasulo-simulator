from prettytable import PrettyTable


class ROBEntry:
    def __init__(self):
        self.instruction = None
        self.finished = False


class ROB:
    def __init__(self, ROBentries):
        self.max_entries = ROBentries
        self.entries = [None]*ROBentries
        self.head_idx = 0
        self.write_idx = 0

    def __str__(self) -> str:
        tbl = PrettyTable(['Entry', 'Instruction', 'Finished'])

        for i in range(self.max_entries):
            if self.entries[i] != None:
                if self.head_idx != i:
                    row = ['ROB{}'.format(i),
                           self.entries[i].instruction.str, self.entries[i].finished]
                else:
                    row = ['\033[92mROB{}\033[0m'.format(i),
                           self.entries[i].instruction.str, self.entries[i].finished]
            else:
                row = ['ROB{}'.format(i), '--', '--']

            tbl.add_row(row)

        return tbl.get_string()

    def is_full(self):
        return (self.write_idx+1) % self.max_entries == self.head_idx

    def allocate_new(self, inst):
        '''
        Creates new ROBEntry
        Returns index of entry
        '''
        assert not self.is_full(), 'You cannot add to a full ROB'

        new = ROBEntry()
        new.instruction = inst
        self.entries[self.write_idx] = new
        ret = self.write_idx
        self.write_idx = (self.write_idx+1) % self.max_entries
        return ret

    def head_ready(self) -> bool:
        return self.entries[self.head_idx] is not None and self.entries[self.head_idx].finished

    def pop_head(self):
        head_inst = self.entries[self.head_idx]
        self.entries[self.head_idx].finished = False
        self.head_idx = (self.head_idx+1) % self.max_entries
        return head_inst
    
    def peak_head(self):
        return self.entries[self.head_idx]
