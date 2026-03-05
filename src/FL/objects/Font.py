from __future__ import annotations

import traceback
from pathlib import Path

from FL.fake.copy import copy_fl_object
from FL.fake.Font import FakeFont
from FL.objects.Encoding import Encoding
from FL.objects.Glyph import Glyph
from FL.objects.Uni import Uni
from FL.objects.WeightVector import WeightVector

__doc__ = "Class to represent a font"


class Font(FakeFont):
    """
    Base class to represent a font
    """

    # Constructor

    def __init__(
        self,
        font_or_path: Font | str | None = None,
        instances: tuple[float, ...] | None = None,
    ) -> None:
        super().__init__()

        # Process params

        if isinstance(font_or_path, Font):
            copy_fl_object(font_or_path, self)
            if instances is not None:
                # Generate an instance
                # instances is a tuple containing instance values for all MM
                # axes defined in the font
                self.ip(instances)

        elif isinstance(font_or_path, str) or isinstance(font_or_path, Path):
            # Instantiate with path
            self.Open(font_or_path)

        # else: Empty font

    def ip(
        self,
        instances: tuple[float, ...],
        family_name: str | None = None,
        style_name: str | None = None,
    ) -> Font:
        f = Font(self)
        f.fake_interpolate(instances, family_name, style_name)
        return f

    def __repr__(self) -> str:
        return "<Font: '%s', %i glyphs>" % (self.full_name, len(self))

    def New(self) -> None:
        """
        Clear the font.
        """
        raise NotImplementedError

    def Open(self, filename: str) -> int:
        """
        Open a font from a VFB file.

        Args:
            filename (str): The path and file name of the VFB file.

        Returns:
            int: 1 on success, 0 if the file could not be opened.

        If you need to import a font (not in VFB format), use `FL.Open()` or
        `FL.OpenFont()`.
        """
        from FL.vfb.reader import VfbToFontReader

        self._set_file_name(None)  # TODO: What if the font already is loaded from disk?
        try:
            reader = VfbToFontReader(Path(filename))
            reader.read(self)
        except Exception:
            print(traceback.format_exc())
            return 0
        self._set_file_name(filename)
        return 1

    def Save(self, filename: str, save_json: bool = True) -> None:
        """
        Save the font in VFB format.

        Args:
            filename (str): The path and file name of the VFB file.
        """
        from FL.vfb.writer import FontToVfbWriter

        self._set_file_name(filename)
        writer = FontToVfbWriter(self)
        if save_json:
            writer.write_json(Path(filename).with_suffix(".vfb.json"))
        writer.write(Path(filename))

    def OpenAFM(self, filename: str, mode: int, layer: int) -> None:
        """
        open AFM-File, mode is the integer bit field.
          The bit list is:
          ALLMETRICS       - 0x0001
          THICKERMETRICS   - 0x0002
          WIDERMETRICS     - 0x0004
          CLOSEMETRICS     - 0x0008
          REPLACEKERNING   - 0x0010
          ADDKERNING       - 0x0020
          AUTOKERNING      - 0x0040
          REPLACEOTHERDATA - 0x0100
          REPLACENAMES     - 0x0200

          Constants for mode (only in FL 4.5 Mac)
          mtALLMETRICS
          mtTHICKERMETRICS
          mtWIDERMETRIC
          mtCLOSEMETRICS
          mtREPLACEKERNING
          mtADDKERNING
          mtAUTOKERNING
          mtREPLACEOTHERDATA
          mtREPLACENAMES
        """
        raise NotImplementedError

    def SaveAFM(self, filename: str) -> None:
        """
        Save an AFM and an INF file.

        Args:
            filename (str): The path and filename to save the files to.
        """
        afm = self.fake_get_afm()
        afm_path = Path(filename).with_suffix(".afm")
        with open(afm_path, "w") as f:
            f.write(afm)
        inf = self.fake_get_inf()
        inf_path = Path(filename).with_suffix(".inf")
        with open(inf_path, "w") as f:
            f.write(inf)

    def Reencode(self, e: Encoding, style: int = 0) -> None:
        """
        Apply an encoding to the font.

        The parameters of this method are not reported by the docstring and I don't know
        what the style parameter does.

        Args:
            e (Encoding): The encoding.
            style (int, optional): _description_. Defaults to 0.
        """
        raise NotImplementedError

    def FindGlyph(self, name_uni_int: str | Uni | int) -> int:
        """
        (name: str) | (unicode: Uni) | (unicode: int)
        - finds glyph and return its index or -1
        """
        if isinstance(name_uni_int, str):
            # name
            for i, g in enumerate(self._glyphs):
                if g.name == name_uni_int:
                    return i
            return -1
        elif isinstance(name_uni_int, Uni):
            # uni object
            for i, g in enumerate(self._glyphs):
                if name_uni_int.value in g.unicodes:
                    return i
            return -1
        elif isinstance(name_uni_int, int):
            # int (unicode value)
            for i, g in enumerate(self._glyphs):
                if name_uni_int in g.unicodes:
                    return i
            return -1
        else:
            raise TypeError

    def DefineAxis(self, name: str, type: str, shortname: str) -> None:
        """
        Defines a new Multiple Master axis.

        Args:
            name (str): The axis name.
            type (str): The axis type: "OpticalSize", "Serif", "Weight", or "Width".
            shortname (str): The two-letter abbreviation.
        """
        if self._axis_count >= 4:
            # Ignore silently
            return

        # tuple is reordered vs. args!
        self._axis.append((name, shortname[:5], type))
        self._axis_count = len(self._axis)

        if self._global_mask is not None:
            self._global_mask.fake_add_axis()

        # Adjust glyphs
        for glyph in self.glyphs:
            glyph.fake_add_axis()

        # Adjust font info

    def DeleteAxis(self, axisindex: int, position: float) -> None:
        """
        Removes the axis. Remaining masters will be blended according to the given
        position.

        Args:
            axisindex (int): The index of the axis to remove (0 to 3).
            position (float): The position of the remaining masters on the removed axis.
        """
        self.fake_remove_axis(axisindex, position, round_values=True)

    def GenerateUnicode(self) -> None:
        """
        Generates Unicode indexes for all glyphs
        """
        raise NotImplementedError

    def GenerateNames(self) -> None:
        """
        Generates names for all glyphs
        """
        raise NotImplementedError

    def GenerateGlyph(self, name: str) -> Glyph:
        """
        Generates new glyph using 'name' as a source of information about glyph's
        composition. See 'FontLabDir/Mapping/alias.dat' for composition definitions.

        Args:
            name (str): _description_

        Returns:
            Glyph: _description_

        The glyph is not added to the font automatically.
        """
        glyph = Glyph()
        glyph.name = name
        return glyph

    def has_key(self, name_uni_int: str | Uni | int) -> int:
        """
        Find a glyph by name, unicode or integer unicode and return 1 (found) or 0 (not
        found).

        Args:
            name_uni_int (str | Uni | int): _description_

        Returns:
            int: 1 if the glyph name or unicode value are present in the font,
                0 otherwise.
        """
        glyph_index = self.FindGlyph(name_uni_int)
        if glyph_index == -1:
            return 0
        return 1

    def GenerateFont(self, fontType: int, filename: str) -> None:
        """
        Generate a font. Deprecated. See the `FL.objects.FontLab` class for a
        description.

        As a method of the `Font` class, this method is deprecated. Since FontLab 4.52
        for Mac and FontLab 4.53 for Windows, `GenerateFont` is a method of the
        `FontLab` class.

        Args:
            fontType (int): The font type.
            filename (str): The path and file name of the generated font.

        Raises:
            AttributeError: In FontLab 5, the method is deprecated.
        """
        raise AttributeError

    # Undocumented methods

    def MakeKernFeature(self, vector: WeightVector) -> None:
        """
        Generates 'kern' feature using font kerning and classes

        Args:
            vector (WeightVector): The `WeightVector` used to interpolate the kerning
                values.
        """
        raise NotImplementedError

    def MergeFonts(self, source: Font, flags: int | None = None) -> None:
        """
        Append all glyphs from the source font to the current fonts.
        Check mfXXXX constants for options.

        Args:
            source (Font): The source font to be merged.
            flags (int | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def SetClassFlags(
        self,
        class_index: int,
        left_lsb: bool | int,
        right_rsb: bool | int,
        width: bool | int | None = None,
    ) -> None:
        """
        (int class_index, bool left, bool right)
        - allows to set 'left' and 'right' properties of the kerning class

        (int class_index, bool lsb, bool rsb, bool width)
        - allows to set 'lsb', 'rsb' and 'width' properties of the metrics class
        """
        self._classes.SetClassFlags(class_index, left_lsb, right_rsb, width)

    def GetClassLeft(self, class_index: int) -> int | None:
        """
        Return the 'left' property of the class.

        Args:
            class_index (int): _description_

        Returns:
            int | None: Returns 0 for non-kerning classes, 0 or 1 for kerning classes,
                None for class_index outside the classes list length.
        """
        return self._classes.GetClassLeft(class_index)

    def GetClassRight(self, class_index: int) -> int | None:
        """
        Return the 'right' property of the class.

        Args:
            class_index (int): _description_

        Returns:
            int | None: Returns 0 for non-kerning classes, 0 or 1 for kerning classes,
                None for class_index outside the classes list length.
        """
        return self._classes.GetClassRight(class_index)

    def GetClassMetricsFlags(self, class_index: int) -> tuple[int, int, int] | None:
        """
        (int class_index)
        - returns the tuple containing LSB, RSB and Width flags of the metrics
        class
        """
        return self._classes.GetClassMetricsFlags(class_index)

    # Additional methods reported by dir(fl.font)

    def GenerateInstance(self, weight_vector: WeightVector) -> None:
        """
        Generate an instance of the font. This method was undocumented, and I couldn't
        figure it out.

        Args:
            weight_vector (WeightVector): _description_
        """
        if not isinstance(weight_vector, WeightVector):
            raise RuntimeError(
                "RuntimeError: Incorrect parameters passed to:\n"
                "  Font.GenerateInstance(WeightVector vector)"
            )
        raise RuntimeError(
            "RuntimeError: Incorrect # of args to:\n"
            "  Font.GenerateInstance(WeightVector vector)"
        )
