from __future__ import annotations

from pathlib import Path


class FakeFont:
    def __init__(self) -> None:
        # Additions for FakeLab

        self._fake_binaries: dict[str, str] = {}
        self.fake_sparse_json = True
        self.fake_deselect_all()

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

    def fake_update(self):
        """
        Is called from FontLab.UpdateFont()
        """
        for index, glyph in enumerate(self.glyphs):
            glyph.fake_update(self, index)

    def fake_deselect_all(self):
        """
        Deselect all glyphs. Is called from FontLab.Unselect().
        """
        self._selection = set()

    def fake_select(self, glyph_index, value=None):
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
        if value:
            self._selection |= {glyph_index}
        else:
            self._selection -= {glyph_index}

    def fake_set_class_flags(self, flags):
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
