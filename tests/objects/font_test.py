import pytest
import unittest

from FL import fl, Font
from pathlib import Path
from vfbLib.vfb.vfb import Vfb


class FontTests(unittest.TestCase):
    def test_instantiation(self):
        f = Font()
        assert isinstance(f, Font)

    def test_instantiation_path(self):
        vfb_path = Path(__file__).parent.parent / "tests" / "data" / "empty.vfb"

        f = Font(vfb_path)
        assert len(fl) == 0
        fl.Add(f)
        assert len(fl) == 1
        assert f.file_name == vfb_path
