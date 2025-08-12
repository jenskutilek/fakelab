import unittest

from vfbLib.enum import G

from FL.objects.Glyph import Glyph
from FL.objects.Point import Point

glyph_a = {
    "name": "a",
    "num_masters": 1,
    "nodes": [
        {"type": "move", "flags": 3, "points": [[(77, 359)]]},
        {"type": "curve", "flags": 3, "points": [[(272, 106), (77, 219), (164, 106)]]},
        {"type": "curve", "flags": 3, "points": [[(468, 359), (380, 106), (468, 219)]]},
        {"type": "curve", "flags": 3, "points": [[(272, 613), (468, 499), (380, 613)]]},
        {"type": "curve", "flags": 3, "points": [[(77, 359), (164, 613), (77, 499)]]},
    ],
    "metrics": [[556, 0]],
    "kerning": {4: [-100]},
    "components": [],
}


class GlyphTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        g = Glyph()
        assert g.parent is None

    def test_deserialize(self) -> None:
        # Deserialize the Glyph object from json.
        g = Glyph()
        g.fake_deserialize(G.Glyph, glyph_a)
        assert g.name == "a"
        assert len(g) == 5  # number of nodes
        assert g.GetMetrics() == Point(556, 0)
        assert len(g.kerning) == 1

        s = g.fake_serialize()
        assert s[G.Glyph] == glyph_a
