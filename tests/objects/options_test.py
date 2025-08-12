import unittest
from pathlib import Path

from FL import Options


def get_reg_path(filename):
    return Path(__file__).parent.parent / "data" / filename


class OptionsTests(unittest.TestCase):
    def test_parse_minimal_ok(self):
        o = Options()

        # Set some values different from the defaults
        o.CacheTTPath = r"C:\Programme\cachett.exe"
        o.ExpandKernCodepage = "Foo"
        o.ExpandKernCount = 1000

        o.fake_load_regfile(get_reg_path("minimal.reg"))

        # Values should have been overwritten
        assert o.CacheTTPath == ""
        assert o.ExpandKernCodepage == "MS Windows 1252 Western (ANSI)"
        assert o.ExpandKernCount == 10919

    def test_parse_full_ok(self):
        o = Options()

        # Set some values different from the defaults
        o.CacheTTPath = r"C:\Programme\cachett.exe"
        o.ExpandKernCodepage = "Foo"
        o.ExpandKernCount = 1000

        o.fake_load_regfile(get_reg_path("Untitled.reg"))

        # Values should have been overwritten
        assert o.CacheTTPath == ""
        assert o.ExpandKernCodepage == "MS Windows 1252 Western (ANSI)"
        assert o.ExpandKernCount == 10919
