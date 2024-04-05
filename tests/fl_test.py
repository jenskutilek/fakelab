import pytest
import unittest

from FL import FakeLab, fl, Font

# fl is pre-instantiated, take care not to modify the global state


class FLTests(unittest.TestCase):
    def test_instantiation(self):
        assert isinstance(fl, FakeLab)

    def test_no_font(self):
        fk = FakeLab()
        assert fk.font is None

    def test_no_font_no_glyph(self):
        fk = FakeLab()
        assert fk.glyph is None

    def test_font_no_glyph(self):
        fk = FakeLab()
        fk.Add(Font())
        assert isinstance(fk.font, Font)
        assert fk.glyph is None
