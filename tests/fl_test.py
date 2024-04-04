import pytest
import unittest

from FL import FakeLab, fl


class FLTests(unittest.TestCase):
    def test_instantiation(self):
        assert isinstance(fl, FakeLab)
