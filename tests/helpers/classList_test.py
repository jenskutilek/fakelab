import unittest

from FL import Font
from FL.helpers.classList import ClassList


class ClassListTests(unittest.TestCase):
    def test_instantiation_empty(self) -> None:
        c = ClassList()
        assert isinstance(c, ClassList)
        assert c._kerning_flags == {}
        assert c._metrics_flags == {}

    def test_instantiation(self) -> None:
        c = ClassList(["_A: A'"])
        assert c == ["_A: A'"]
        assert c._kerning_flags == {}
        assert c._metrics_flags == {}

    def test_instantiation_flags(self) -> None:
        c = ClassList(["_A: A'"])
        c.SetClassFlags(0, True, True)
        assert c == ["_A: A'"]
        assert c._kerning_flags == {"_A": (3072, 0)}
        assert c._metrics_flags == {}

    def test_set(self) -> None:
        c = ClassList(["_A: A'"])
        c.SetClassFlags(0, True, True)
        assert c == ["_A: A'"]
        assert c._kerning_flags == {"_A": (3072, 0)}
        assert c._metrics_flags == {}

        # Simulate setting the full list to a new value by calling fake_set_classes
        # (This is usually called from the font, Font.classes = [...])

        c.fake_set_classes(["_A: A'", "_B: B'"])
        assert c._kerning_flags == {"_A": (3072, 0)}
        assert c._metrics_flags == {}
        c.SetClassFlags(1, True, False)
        assert c._kerning_flags == {"_A": (3072, 0), "_B": (1024, 0)}
        assert c._metrics_flags == {}

        # When passing a longer or shorter list, the flags stay the same, even for
        # classes that are not present anymore
        c.fake_set_classes(["_B: B'"])
        assert c._kerning_flags == {"_A": (3072, 0), "_B": (1024, 0)}
        assert c._metrics_flags == {}

    def test_add(self) -> None:
        c1 = ClassList(["_A: A'"])
        c1.SetClassFlags(0, True, False)
        c2 = ["_O: O'"]
        assert c1 == ["_A: A'"]
        assert c1._kerning_flags == {"_A": (1024, 0)}
        assert c1._metrics_flags == {}
        c3 = c1 + c2
        assert c3 == ["_A: A'", "_O: O'"]
        assert c3._kerning_flags == {"_A": (1024, 0)}
        assert c3._metrics_flags == {}
        assert id(c1) != id(c3)

    def test_iadd(self) -> None:
        c1 = ClassList(["_A: A'"])
        c1.SetClassFlags(0, True, False)
        id1 = id(c1)
        c2 = ["_O: O'"]
        assert c1 == ["_A: A'"]
        assert c1._kerning_flags == {"_A": (1024, 0)}
        assert c1._metrics_flags == {}
        c1 += c2
        assert c1 == ["_A: A'", "_O: O'"]
        assert c1._kerning_flags == {"_A": (1024, 0)}
        assert c1._metrics_flags == {}
        assert id1 == id(c1)

    def test_font(self) -> None:
        f = Font()
        f.classes = ["a: a"]
        assert isinstance(f.classes, list)
        assert isinstance(f._classes, ClassList)
        assert f._classes._kerning_flags == {}
        assert f._classes._metrics_flags == {}

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
