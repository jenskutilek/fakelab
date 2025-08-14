import unittest
from pathlib import Path
from unittest import mock

from FL.objects.Options import Options


def get_reg_path(filename: str) -> Path:
    return Path(__file__).parent.parent / "data" / filename


class OptionsTests(unittest.TestCase):
    def setUp(self) -> None:
        Path.home = mock.MagicMock()
        Path.home.return_value = Path(__file__).parent.parent / "data"

    def test_parse_minimal_ok(self) -> None:
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

    def test_parse_full_ok(self) -> None:
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

    def test_persist_options(self) -> None:
        options_path = Path().home() / ".fakelab"
        options_path.unlink(missing_ok=True)
        o = Options()
        # Options should have been loaded from data/.fakelab
        assert o.TTIScale1000 == 0
        o.TTIScale1000 = 1
        del o
        # Options should have been saved to data/.fakelab, verify by instantiating again
        o = Options()
        # Previously changed setting should be as we set it
        assert o.TTIScale1000 == 1
