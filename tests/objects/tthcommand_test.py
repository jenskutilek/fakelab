import unittest

import pytest

from FL.objects.TTHCommand import TTHCommand


class TTHCommandTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        # No args
        with pytest.raises(RuntimeError):
            TTHCommand()

    def test_instantiation_args(self) -> None:
        # Initialize with code and one param
        t = TTHCommand(1, 1, 2)
        assert t.code == 1
        assert t.params == [1, 2]
        assert str(t) == "<TTHCommand: ALIGNTOP(1, 2)>"

    def test_instantiation_args_too_many(self) -> None:
        # Initialize with code and too many params
        # The message says one command and up to 5 integer params, but the error is
        # thrown at 1 + 4 params already.
        with pytest.raises(RuntimeError):
            TTHCommand(1, 1, 2, 3, 4, 5)
