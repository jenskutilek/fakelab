import pytest
import unittest

from FL import Font
from FL.helpers.classList import ClassList


class ClassListTests(unittest.TestCase):
    def test_instantiation_empty(self):
        c = ClassList()
        assert isinstance(c, ClassList)
        assert c._flags == []

    def test_instantiation(self):
        c = ClassList(["_A: A'"])
        assert c == ["_A: A'"]
        assert c._flags == [0]

    def test_instantiation_flags(self):
        c = ClassList(["_A: A'"])
        c.SetClassFlags(0, True, True)
        assert c == ["_A: A'"]
        assert c._flags == [3072]

        # When we pass the flags to __init__, they should persist
        c = ClassList(["_A: A'", "_O: O'"], c._flags)
        assert c._flags == [3072, 0]

        # When passing a shorter list, the flags list should be truncated
        c = ClassList(["_A: A'"], c._flags)
        assert c._flags == [3072]

    def test_add(self):
        c1 = ClassList(["_A: A'"])
        c2 = ["_O: O'"]
        assert c1 == ["_A: A'"]
        assert c1._flags == [0]
        c3 = c1 + c2
        assert c3 == ["_A: A'", "_O: O'"]
        assert c3._flags == [0, 0]
        assert id(c1) != id(c3)

    def test_iadd(self):
        c1 = ClassList(["_A: A'"])
        id1 = id(c1)
        c2 = ["_O: O'"]
        assert c1 == ["_A: A'"]
        assert c1._flags == [0]
        c1 += c2
        assert c1 == ["_A: A'", "_O: O'"]
        assert c1._flags == [0, 0]
        assert id1 == id(c1)

    def test_font(self):
        f = Font()
        f.classes = ["a"]
        assert isinstance(f.classes, list)
        assert isinstance(f._classes, ClassList)
        assert f._classes._flags == [0]

    def test_font_add(self):
        f = Font()
        f.classes += "b"
        assert f.classes == ["b"]
        assert f.GetClassLeft(0) == 0
        assert f.GetClassRight(0) == 0
        f.classes += "c"
        assert f.classes == ["b", "c"]
        assert f.GetClassLeft(1) == 0
        assert f.GetClassRight(1) == 0
        assert f.GetClassLeft(2) is None
        assert f.GetClassRight(2) is None

    def test_font_iadd(self):
        f = Font()
        f.classes = f.classes + ["b"]
        assert f.classes == ["b"]
        assert f.GetClassLeft(0) == 0
        assert f.GetClassRight(0) == 0
        f.classes = f.classes + ["c"]
        assert f.classes == ["b", "c"]
        assert f.GetClassLeft(1) == 0
        assert f.GetClassRight(1) == 0
        assert f.GetClassLeft(2) is None
        assert f.GetClassRight(2) is None

    def test_font_append(self):
        # Append has no effect
        f = Font()
        f.classes.append("b")
        assert len(f.classes) == 0

    def test_font_extend(self):
        # Extend has no effect
        f = Font()
        f.classes.extend(["b"])
        assert len(f.classes) == 0

    def test_font_insert(self):
        # Insert has no effect
        f = Font()
        f.classes.insert(0, "b")
        assert len(f.classes) == 0
