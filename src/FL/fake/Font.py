from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.fake.Kerning import FakeKerning

if TYPE_CHECKING:
    from FL.objects.Uni import Uni


class FakeFont(Copyable):

    __slots__ = [
        "_fake_binaries",
        "_fake_kerning",
        "_file_name",
        "_selection",
        "fake_sparse_json",
    ]

    def __init__(self) -> None:
        # Additions for FakeLab

        self._fake_binaries: dict[str, str] = {}
        self._fake_kerning = FakeKerning(self)
        self.fake_sparse_json = True
        self.fake_deselect_all()

    # Additional properties for FakeLab

    @property
    def fake_kerning(self) -> FakeKerning:
        """
        Returns the `FL.fake.FakeKerning` object, which can be used to manipulate the
        font's kerning data.
        """
        return self._fake_kerning

    # Additions for FakeLab

    def fake_binary_get(self, fontType: int) -> bytes:
        binary_path = self._fake_binaries[str(fontType)]
        with open(binary_path, "rb") as f:
            binary = f.read()
        return binary

    def fake_binary_from_path(self, fontType: int, file_path: str) -> None:
        """
        Assign a binary file from a path. This will be used to fake the
        FakeLab.GenerateFont() method.
        """
        # Convert key to str because JSON needs it
        self._fake_binaries[str(fontType)] = file_path

    def fake_update(self) -> None:
        """
        Is called from FontLab.UpdateFont()
        """
        for index, glyph in enumerate(self.glyphs):
            glyph.fake_update(self, index)

    def fake_deselect_all(self) -> None:
        """
        Deselect all glyphs. Is called from FontLab.Unselect().
        """
        self._selection: set[int] = set()

    def fake_select(self, gid: str | Uni | int, value: bool | None = None) -> None:
        """
        Change selection status for glyph_index.
        >>> f = Font()
        >>> f.fake_select(1, False)
        >>> print(f._selection)
        set()
        >>> f.fake_select(1, True)
        >>> print(f._selection)
        {1}
        >>> f.fake_select(3, True)
        >>> print(f._selection)
        {1, 3}
        >>> f.fake_select(2, False)
        >>> print(f._selection)
        {1, 3}
        >>> f.fake_select(1, False)
        >>> print(f._selection)
        {3}
        """
        if isinstance(gid, int):
            glyph_index = gid
        elif isinstance(gid, Uni) or isinstance(gid, str):
            glyph_index = self.FindGlyph(gid)
        if glyph_index > -1:
            if value:
                self._selection |= {glyph_index}
            else:
                self._selection -= {glyph_index}

    def fake_set_class_flags(self, flags: list[str]) -> None:
        """
        Set the kerning class flags from a list of str ("L", "R", "LR", ...)
        """
        # FIXME: In the vfb, the flags are stored as tuples of two values. The second
        # value is 0, it's not clear what it represents. Maybe the width flag for
        # metrics classes?
        for i, f in enumerate(flags):
            self.SetClassFlags(i, "L" in f, "R" in f)

    def _set_file_name(self, filename: str | Path | None) -> None:
        """
        Make sure the file name (actually, the path) is stored as Path
        """
        if filename is None:
            self._file_name = None
            return

        self._file_name = Path(filename) if not isinstance(filename, Path) else filename
