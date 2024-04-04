import pytest
import unittest

from FL import Font


class FontTests(unittest.TestCase):
    def test_instantiation(self):
        f = Font()
        assert isinstance(f, Font)
