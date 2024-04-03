from __future__ import annotations

from FL.helpers.FLList import FLList
from FL.objects import TTHPoint
from FL.objects.Glyph import Glyph
from FL.objects.Hint import Hint
from FL.objects.Point import Point
from FL.objects.TTHCommand import TTHCommand
from typing import List


class TTH(object):
    def __init__(self, g=None, f=None):
        self.glyph = g
        self.font = f

        self.top_zones: List[Hint] = FLList()
        self.bottom_zones: List[Hint] = FLList()
        self.base_top_zones: List[Hint] = FLList()
        self.base_bottom_zones: List[Hint] = FLList()
        self.hstems: List[int] = FLList()
        self.vstems: List[int] = FLList()
        self.base_hstems: List[int] = FLList()
        self.base_vstems: List[int] = FLList()
        self.zero_point = Point(0, 0)
        self.upm = 1000
        self.ppm = None  # FL returns a random number
        self.outline: List[TTHPoint] = FLList()
        self.base_outline: List[TTHPoint] = FLList()
        self.commands: List[TTHCommand] = FLList()
        self.problems = FLList()

    # Attributes

    # Operations

    def __len__(self):
        """
        returns number of commands
        """
        return len(self.commands)

    def __getitem__(self, index):
        """
        accesses TTCommand list
        """
        return self.commands[index]

    # Methods

    def Init(self):
        raise NotImplementedError

    def Initoutline(self):
        raise NotImplementedError

    def SetPPM(self):
        raise NotImplementedError

    def ResetProgram(self):
        raise NotImplementedError

    def LoadProgram(self, glyph: Glyph | None = None):
        raise NotImplementedError

    def SaveProgram(self):
        raise NotImplementedError

    def SortProgram(self):
        raise NotImplementedError

    def RunProgram(self):
        raise NotImplementedError

    def RunCommand(self):
        raise NotImplementedError

    def TestProgram(self):
        raise NotImplementedError

    def BuildFromLinks(self):
        raise NotImplementedError

    def ResetFinalDeltas(self):
        raise NotImplementedError

    def ResetAllDeltas(self):
        raise NotImplementedError

    def LoadFromTextFile(self):
        raise NotImplementedError

    def SaveToTextFile(self):
        raise NotImplementedError
