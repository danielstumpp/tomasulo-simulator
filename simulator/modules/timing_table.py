"""Timing table class and related parsers"""

from typing import List
from simulator.modules.instruction import Instruction
from simulator.modules.state import State


class TimingTable:
    """Timing table class for easy testing and comparison"""

    def __init__(self) -> None:
        self.issue = []
        self.ex_start = []
        self.ex_end = []
        self.write_back = []
        self.commit = []

    @classmethod
    def fromState(state: State) -> None:
        pass
