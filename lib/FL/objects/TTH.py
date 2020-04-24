class TTH(object):
    def __init__(self, g=None, f=None):
        self.glyph = g
        self.font = f

        self.top_zones = None
        self.bottom_zones = None
        self.base_top_zones = None
        self.base_bottom_zones = None
        self.hstems = None
        self.vstems = None
        self.base_hstems = None
        self.base_vstems = None
        self.zero_point = None
        self.upm = None
        self.ppm = None
        self.outline = None
        self.base_outline = None
        self.commands = None
        self.problems = None

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

    def LoadProgram(self):
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
