import unittest

from FL.helpers.math import int32_to_unsigned, uint32_to_signed

s1 = -458254122
u1 = 3836713174

s2 = 2082841200
u2 = 2082841200


class MathTest(unittest.TestCase):
    def test_signed_to_unsigned_1(self) -> None:
        assert int32_to_unsigned(0) == 0

    def test_signed_to_unsigned_2(self) -> None:
        assert int32_to_unsigned(s1) == u1

    def test_signed_to_unsigned_3(self) -> None:
        assert int32_to_unsigned(s2) == u2

    def test_unsigned_to_signed_1(self) -> None:
        assert uint32_to_signed(0) == 0

    def test_unsigned_to_signed_2(self) -> None:
        assert uint32_to_signed(u1) == s1

    def test_unsigned_to_signed_3(self) -> None:
        assert uint32_to_signed(u2) == s2
