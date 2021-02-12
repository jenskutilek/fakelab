import pytest

from FL import fl, Component, Font, Glyph, Point
from fakeLabDemo.selection.composites import selectComposites


def test_selectComposites():
    # Construct a fake FontLab font object
    font = Font()
    g = Glyph(1)
    g.name = "A"
    g.width = 500
    g.unicode = 0x41
    font.glyphs.append(g)

    g = Glyph(1)
    g.name = "dieresis"
    g.width = 500
    g.unicode = 0xA8
    font.glyphs.append(g)

    g = Glyph(1)
    g.name = "Adieresis"
    g.width = 500
    g.unicode = 0xC4
    g.components.append(Component(0))
    g.components.append(Component(1, Point(0, 300)))
    font.glyphs.append(g)

    # Add the font to the FL object
    fl.Add(font)
    fl.UpdateFont()

    # Run our script to be tested on the font
    selectComposites(fl.font)

    # You could save the fake font to JSON instead of VFB.
    # fl.font.Save("test_composites.vfb.json")

    # Test if the correct glyphs have been selected
    assert fl.Selected(0) == 0
    assert fl.Selected(1) == 0
    assert fl.Selected(2) == 1

    # Close the fake font
    fl.Close()
