import pytest
import unittest

from FL.helpers.nametables import StandardNametable

nt = StandardNametable()


class StandardNametableTest(unittest.TestCase):
    # Unicode to Name

    def test_uni_0(self):
        assert nt.get_name_for_unicode(0) == "NULL"

    def test_uni_65(self):
        assert nt.get_name_for_unicode(65) == "A"

    def test_uni_0x26b8(self):
        assert nt.get_name_for_unicode(0x26B8) == "uni26B8"

    def test_uni_0x1F60E(self):
        assert nt.get_name_for_unicode(0x1F60E) == "u1F60E"

    def test_uni_0x1F60EF(self):
        # longer
        assert nt.get_name_for_unicode(0x1F60EF) == "u1F60EF"

    # Name to Unicode

    def test_name_A(self):
        assert nt.get_unicode_for_name("A") == 65

    def test_name_union(self):
        assert nt.get_unicode_for_name("union") == 0x222A

    def test_name_dotnull(self):
        assert nt.get_unicode_for_name(".null") == 0

    def test_name_dotNUL(self):
        # not present
        assert nt.get_unicode_for_name(".NUL") == -1

    def test_name_NUL(self):
        assert nt.get_unicode_for_name("NUL") == 0

    def test_name_NULL(self):
        assert nt.get_unicode_for_name("NULL") == 0

    def test_name_uni(self):
        assert nt.get_unicode_for_name("uniFEFF") == 0xFEFF

    def test_name_0x1F60E(self):
        assert nt.get_unicode_for_name("u1F60E") == 0x1F60E

    def test_name_0x1F60EF(self):
        assert nt.get_unicode_for_name("u1F60EF") == 0x1F60EF

    def test_name_0x1F60EJ(self):
        # nan
        assert nt.get_unicode_for_name("u1F60EJ") == -1
