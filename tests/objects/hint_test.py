import unittest

import pytest

from FL.objects.Glyph import Glyph
from FL.objects.Hint import Hint


class HintTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        h = Hint()
        assert h.parent is None
        assert h.position == 0
        assert h.width == 21
        assert h.positions == [0] * 16
        assert h.widths == [21] * 16

    def test_instantiation_copy_extra(self) -> None:
        h0 = Hint(-1, 100)
        h = Hint(h0)
        assert h.parent is None
        assert h.position == -1
        assert h.width == 100
        assert h.positions == [-1] * 16
        assert h.widths == [100] * 16

    def test_instantiation_copy(self) -> None:
        h0 = Hint(-1, 100)
        with pytest.raises(TypeError):
            # When the second arg is an int, the first one must be as well
            Hint(h0, 1)

    def test_position_affects_mm(self) -> None:
        h = Hint()
        h.position = 50
        assert h.position == 50
        assert h.positions == [50] * 16

    def test_width_affects_mm(self) -> None:
        h = Hint()
        h.width = 50
        assert h.width == 50
        assert h.widths == [50] * 16
