class TTHCommand(object):
    def __init__(self, code, params):
        self.code = code
        self._params = params

    # Attributes

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def params(self):
        return self._params
