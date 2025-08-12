import unittest

import pytest

from FL.objects.KerningPair import KerningPair


class KerningPairTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        k = KerningPair()
        assert k.parent is None
        assert k.key == 0
        assert k.value == 0
        assert k.values == [0] * 16
