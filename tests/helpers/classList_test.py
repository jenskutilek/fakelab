import unittest

from FL import Font
from FL.helpers.classList import ClassList


class ClassListTests(unittest.TestCase):
    def test_instantiation_empty(self) -> None:
        c = ClassList()
        assert isinstance(c, ClassList)
        assert c._flags == []

    def test_instantiation(self) -> None:
        c = ClassList(["_A: A'"])
        assert c == ["_A: A'"]
        assert c._flags == [0]

    def test_instantiation_flags(self) -> None:
        c = ClassList(["_A: A'"])
        c.SetClassFlags(0, True, True)
        assert c == ["_A: A'"]
        assert c._flags == [3072]

        # When we pass the old list to __init__, the flags should persist
        c = ClassList(["_A: A'", "_B: B'"], old_list=c)
        assert c._flags == [3072, 0]
        c.SetClassFlags(1, True, False)
        assert c._flags == [3072, 1024]

        # When passing a longer or shorter list, the length of the flags list should be
        # adapted and the existing classes should keep their flags even though the index
        # changes
        c = ClassList(["_B: B'"], old_list=c)
        assert c._flags == [1024]

    def test_add(self) -> None:
        c1 = ClassList(["_A: A'"])
        c2 = ["_O: O'"]
        assert c1 == ["_A: A'"]
        assert c1._flags == [0]
        c3 = c1 + c2
        assert c3 == ["_A: A'", "_O: O'"]
        assert c3._flags == [0, 0]
        assert id(c1) != id(c3)

    def test_iadd(self) -> None:
        c1 = ClassList(["_A: A'"])
        id1 = id(c1)
        c2 = ["_O: O'"]
        assert c1 == ["_A: A'"]
        assert c1._flags == [0]
        c1 += c2
        assert c1 == ["_A: A'", "_O: O'"]
        assert c1._flags == [0, 0]
        assert id1 == id(c1)

    def test_font(self) -> None:
        f = Font()
        f.classes = ["a: a"]
        assert isinstance(f.classes, list)
        assert isinstance(f._classes, ClassList)
        assert f._classes._flags == [0]

    def test_font_add(self) -> None:
        f = Font()
        f.classes += ["b: b"]
        assert f.classes == ["b: b"]
        assert f.GetClassLeft(0) == 0
        assert f.GetClassRight(0) == 0
        f.classes += ["c: c"]
        assert f.classes == ["b: b", "c: c"]
        assert f.GetClassLeft(1) == 0
        assert f.GetClassRight(1) == 0
        assert f.GetClassLeft(2) is None
        assert f.GetClassRight(2) is None

    def test_font_iadd(self) -> None:
        f = Font()
        f.classes = f.classes + ["b: b"]
        assert f.classes == ["b: b"]
        assert f.GetClassLeft(0) == 0
        assert f.GetClassRight(0) == 0
        f.classes = f.classes + ["c: c"]
        assert f.classes == ["b: b", "c: c"]
        assert f.GetClassLeft(1) == 0
        assert f.GetClassRight(1) == 0
        assert f.GetClassLeft(2) is None
        assert f.GetClassRight(2) is None

    def test_font_append(self) -> None:
        # Append has no effect
        f = Font()
        f.classes.append("b: b")
        assert len(f.classes) == 0

    def test_font_extend(self) -> None:
        # Extend has no effect
        f = Font()
        f.classes.extend(["b: b"])
        assert len(f.classes) == 0

    def test_font_insert(self) -> None:
        # Insert has no effect
        f = Font()
        f.classes.insert(0, "b: b")
        assert len(f.classes) == 0
