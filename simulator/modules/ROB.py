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

    def is_full(self):
        return (self.write_idx+1)%self.max_entries == self.head_idx

    def allocate_new(self):
        '''
        Creates new ROBEntry
        Returns index of entry
        '''
        assert not self.is_full(), 'You cannot add to a full ROB'

        new = ROBEntry()
        self.entries[self.write_idx] = new
        ret = self.write_idx
        self.write_idx = (self.write_idx+1) % self.max_entries
        return ret
