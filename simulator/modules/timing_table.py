"""Timing table class and related parsers"""

from simulator.modules.instruction import Instruction
from simulator.modules.state import State
from prettytable import PrettyTable
import csv


class TimingTable:
    """Timing table class for easy testing and comparison"""

    def __init__(self) -> None:
        self.issue = []
        self.ex_start = []
        self.ex_end = []
        self.mem = []
        self.write_back = []
        self.commit = []

    def __eq__(self, other) -> bool:
        """ Overloaded equality operator to compare timing tables"""
        if type(self) != type(other):
            return False

        len_valid = ((len(self.issue) == len(other.issue)) and
                     (len(self.ex_start) == len(other.ex_start)) and
                     (len(self.ex_end) == len(other.ex_end)) and
                     (len(self.mem) == len(other.mem)) and
                     (len(self.write_back) == len(other.write_back)) and
                     (len(self.commit) == len(other.commit)))

        if len_valid:
            # find and replace '-' with None in all entries
            self._standardize_format()
            other._standardize_format()

            vals_valid = ((self.issue == other.issue) and
                          (self.ex_start == other.ex_start) and
                          (self.ex_end == other.ex_end) and
                          (self.mem == other.mem) and
                          (self.write_back == other.write_back) and
                          (self.commit == other.commit))

            return vals_valid
        else:
            return False

    def __str__(self) -> str:
        """timing table string for print() calls"""
        tbl = PrettyTable(['','ISSUE', 'EX', 'MEM', 'WB', 'COMMIT'])
        self._standardize_format()

        for i in range(len(self.issue)):
            row = ['I{}'.format(i), self.issue[i], self.ex_start[i]+'-'+self.ex_end[i],
                   self.mem[i], self.write_back[i], self.commit[i]]
            tbl.add_row(row)

        return tbl.get_string()

    def load_from_state(self, state: State) -> bool:
        """Loads the Timing table from an existing state"""

        for i in range(len(state.instructions)):
            inst = state.instructions[i]
            self.issue.append(inst.issue_cycle)
            self.ex_start.append(inst.execute_cycle_start)
            self.ex_end.append(inst.execute_cycle_end)
            self.mem.append(inst.mem_cycle)
            self.write_back.append(inst.writeback_cycle)
            self.commit.append(inst.commit_cycle)

        return True

    def load_from_file(self, filename: str) -> bool:
        """loads the timing table from a CSV-style file"""

        try:
            csv_file = open(filename, newline='')
        except:
            print("ERROR: asm file -- " +
                  filename + " -- could not be opened!")
            return False

        try:
            reader = csv.reader(csv_file, delimiter=',')
        except:
            print("ERROR: could not read timing table file")
            return False

        reader_list = list(reader)
        for line in reader_list:
            if len(line) != 6:
                print('ERROR: invalid timing table from file')
                return False

            self.issue.append(str(line[0].strip()))
            self.ex_start.append(str(line[1].strip()))
            self.ex_end.append(str(line[2].strip()))
            self.mem.append(str(line[3].strip()))
            self.write_back.append(str(line[4].strip()))
            self.commit.append(str(line[5].strip()))

    def _standardize_format(self) -> None:
        self.issue = [str(v).replace('None', '-') for v in self.issue]
        self.ex_start = [str(v).replace('None', '-') for v in self.ex_start]
        self.ex_end = [str(v).replace('None', '-') for v in self.ex_end]
        self.mem = [str(v).replace('None', '-') for v in self.mem]
        self.write_back = [str(v).replace('None', '-')
                           for v in self.write_back]
        self.commit = [str(v).replace('None', '-') for v in self.commit]
