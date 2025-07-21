from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from vfbLib.parsers.text import OpenTypeStringParser

from FL.fake.Base import Copyable
from FL.fake.Kerning import FakeKerning
from FL.objects.Feature import Feature
from FL.objects.Guide import Guide

if TYPE_CHECKING:
    from vfbLib.typing import GuidePropertyList, MMGuidesDict

    from FL.objects.Uni import Uni


class FakeFont(Copyable):
    __slots__ = [
        "_fake_binaries",
        "_fake_kerning",
        "_file_name",
        "_selection",
        "fake_sparse_json",
        "fake_vfb_object",
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

    def fake_deserialize_axis(self, data: str) -> None:
        self.axis.append((data, data[:2], data))

    def fake_serialize_axis(self) -> list[str]:
        names = []
        for axis in self.axis:
            long, _, _ = axis
            names.append(long)
        return names

    def fake_deserialize_features(self, features: list[str]) -> None:
        self._features.clean()
        features_dict = OpenTypeStringParser.build_fea_dict(features)
        prefix = features_dict.get("prefix")
        if prefix:
            self.ot_classes = "\n".join(prefix)
        for feature_dict in features_dict.get("features", []):
            feature = Feature(feature_dict["tag"], "\n".join(feature_dict["code"]))
            self.features.append(feature)

    def fake_serialize_features(self) -> list[str]:
        fea = []
        if self.ot_classes:
            fea.extend(self.ot_classes.splitlines())
            # FIXME: Do we need empty lines as separator?
        for feature in self.features:
            fea.append("feature %s {" % feature.tag)
            fea.extend(feature.value.splitlines())
            fea.append("} %s;" % feature.tag)
        return fea

    def fake_deserialize_guides(self, data: MMGuidesDict) -> None:
        for k, target in (("h", self.hguides), ("v", self.vguides)):
            if dir_master_guides := data[k]:
                first_master_guides = dir_master_guides[0]
                num_guides = len(first_master_guides)
                for guide_dict in first_master_guides:
                    g = Guide(guide_dict["pos"], guide_dict["angle"])
                    target.append(g)
                for master_index in range(1, self._masters_count):
                    for guide_index in range(num_guides):
                        guide_dict = dir_master_guides[master_index][guide_index]
                        target[guide_index].position.append(guide_dict["pos"])
                        target[guide_index].angle.append(guide_dict["angle"])

    def fake_serialize_guides(self): ...

    def fake_deserialize_guide_properties(self, data: GuidePropertyList) -> None:
        for guide_prop_dict in data:
            # Index over h + v: # FIXME
            guide_index = guide_prop_dict["index"]
            color = guide_prop_dict.get("color")
            if color:
                self.hguides[guide_index]._color = color
            name = guide_prop_dict.get("name")
            if name:
                self.hguides[guide_index]._name = name

    def fake_serialize_guide_properties(self): ...
