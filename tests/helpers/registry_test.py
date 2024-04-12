import pytest
import unittest

from FL.helpers.registry import parse_registry_file
from pathlib import Path


def get_reg_path(filename):
    return Path(__file__).parent.parent / "data" / filename


class RegistryTests(unittest.TestCase):
    def test_parse_ok(self):
        reg = parse_registry_file(get_reg_path("minimal.reg"))
        assert reg == {
            "CacheTTPath": "",
            "ExpandKernCodepage": "MS Windows 1252 Western (ANSI)",
            "ExpandKernCount": 10919,
        }

    def test_parse_empty(self):
        with pytest.raises(EOFError):
            parse_registry_file(get_reg_path("empty.reg"))

    def test_parse_no_key(self):
        with pytest.raises(ValueError):
            parse_registry_file(get_reg_path("nokey.reg"))

    def test_parse_wrong_header(self):
        with pytest.raises(AssertionError):
            parse_registry_file(get_reg_path("wrong_header.reg"))

    def test_parse_wrong_value_type(self):
        with pytest.raises(AssertionError):
            parse_registry_file(get_reg_path("wrong_value_type.reg"))
