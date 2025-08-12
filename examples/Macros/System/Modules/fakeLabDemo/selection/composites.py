from __future__ import absolute_import, division, print_function

from FL import fl


def getFontIndex(font):
    """
    Get the index of the supplied font.
    We must iterate through the open fonts and compare file names,
    because the == operator can not compare the font objects directly.
    (FL font objects get a different id() each time they are called)

    :param font: A title for the dialog.
    :type font:  :py:class:`FL.Font`
    """
    for i in range(len(fl)):
        cf = fl[i]
        if cf.file_name == font.file_name:
            if font.file_name is None:
                if (
                    cf.family_name == font.family_name
                    and cf.style_name == font.style_name
                ):
                    return (cf, i)
            else:
                return (cf, i)
    # Font was not found, probably there are no open fonts
    return (None, -1)


def setSelection(font, glyph_names):
    """
    Set glyphs from the glyph_names list as selected in the font window.
    """
    f, i = getFontIndex(font)
    if i > -1:
        fl.ifont = i
        fl.Unselect()
        for n in glyph_names:
            fl.Select(n)


def selectComposites(font):
    """
    Select composites in font.
    """
    setSelection(font, [glyph.name for glyph in font.glyphs if glyph.components])
