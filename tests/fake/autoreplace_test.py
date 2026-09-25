from time import time
from unittest import TestCase

from vfbLib.enum import G
from vfbLib.typing import GlyphData, MMNode

from FL import Font, Glyph, Hint
from FL.fake.autoreplace import autoreplace_glyph, do_hints_overlap
from FL.objects.Replace import TYPE_HORIZONTAL_HINT, TYPE_NODE, TYPE_VERTICAL_HINT

vfb_glyph = GlyphData(
    name="n",
    num_masters=1,
    nodes=[
        MMNode(type="move", flags=0, points=[[(600, 0)]]),
        MMNode(type="line", flags=0, points=[[(600, 30)]]),
        MMNode(
            type="curve",
            flags=0,
            points=[[(532, 60), (600, 30), (569, 49)]],
        ),
        MMNode(
            type="curve",
            flags=3,
            points=[[(537, 285), (532, 60), (537, 154)]],
        ),
        MMNode(
            type="curve",
            flags=3,
            points=[[(376, 507), (537, 435), (485, 507)]],
        ),
        MMNode(
            type="curve",
            flags=0,
            points=[[(202, 397), (288, 507), (226, 456)]],
        ),
        MMNode(type="line", flags=0, points=[[(200, 397)]]),
        MMNode(
            type="curve",
            flags=0,
            points=[[(207, 501), (200, 397), (207, 439)]],
        ),
        MMNode(
            type="curve",
            flags=0,
            points=[[(38, 489), (111, 504), (38, 489)]],
        ),
        MMNode(type="line", flags=0, points=[[(38, 458)]]),
        MMNode(
            type="curve",
            flags=0,
            points=[[(114, 439), (83, 450), (114, 439)]],
        ),
        MMNode(type="line", flags=0, points=[[(114, 60)]]),
        MMNode(type="curve", flags=0, points=[[(38, 30), (72, 49), (38, 30)]]),
        MMNode(type="line", flags=0, points=[[(38, 0)]]),
        MMNode(type="line", flags=0, points=[[(275, 0)]]),
        MMNode(type="line", flags=0, points=[[(275, 29)]]),
        MMNode(
            type="curve",
            flags=0,
            points=[[(208, 59), (275, 29), (244, 47)]],
        ),
        MMNode(type="line", flags=1, points=[[(208, 278)]]),
        MMNode(
            type="curve",
            flags=3,
            points=[[(341, 444), (208, 357), (256, 444)]],
        ),
        MMNode(
            type="curve",
            flags=3,
            points=[[(442, 260), (420, 444), (442, 372)]],
        ),
        MMNode(
            type="curve",
            flags=0,
            points=[[(438, 59), (442, 147), (438, 59)]],
        ),
        MMNode(
            type="curve",
            flags=0,
            points=[[(371, 29), (402, 47), (371, 29)]],
        ),
        MMNode(type="line", flags=0, points=[[(371, 0)]]),
    ],
    metrics=[(629, 0)],
    hints={
        "v": [[{"pos": 114, "width": 94}], [{"pos": 442, "width": 95}]],
        "h": [
            [{"pos": 444, "width": 63}],
            [{"pos": 0, "width": 30}],
            [{"pos": 439, "width": 62}],
        ],
    },
)

# fmt:off
totally_random = [
    (728, 26), (705, 32), (100, 116), (-97, 39), (666, 98), (155, 59), (478, 10),
    (-33, 78), (538, 75), (172, 102), (-178, 118), (789, 62), (43, 63), (-6, 29),
    (354, 120), (-156, 97), (395, 21), (-79, 31), (608, 22), (-86, 36), (248, 14),
    (649, 91), (287, 112), (740, 20), (759, 86), (-18, 99), (671, 17), (442, 18),
    (-99, 74), (-62, 92), (423, 103), (103, 60), (149, 69), (469, 36), (727, 24),
    (26, 6), (621, 69), (283, 116), (54, 33), (548, 42), (-126, 35), (-117, 13),
    (472, 98), (-43, 117), (14, 104), (315, 82), (745, 80), (63, 73), (143, 32),
    (293, 23), (-154, 36), (410, 53), (395, 97), (212, 57), (-20, 10), (318, 18),
    (376, 16), (718, 100), (732, 94), (543, 7), (132, 18), (289, 51), (723, 115), 
    (713, 62), (711, 36), (161, 87), (639, 96), (-43, 94), (112, 48), (232, 4),
    (494, 20), (623, 93), (643, 20), (208, 38), (532, 103), (229, 80), (505, 17),
    (746, 86), (-89, 108), (563, 56), (-106, 99), (376, 29), (527, 71), (527, 5),
    (372, 49), (161, 23), (262, 95), (190, 1), (481, 0), (492, 81), (73, 86), (43, 30),
    (509, 97), (-57, 76), (-24, 34), (778, 19), (786, 93), (167, 3), (428, 58),
    (512, 79)
]

non_overlap = [
    (34, 1), (90, 1), (196, 1), (20, 1), (142, 1), (112, 1), (42, 1), (70, 1), (76, 1),
    (114, 1), (48, 1), (116, 1), (132, 1), (162, 1), (124, 1), (4, 1), (50, 1),
    (184, 1), (150, 1), (14, 1), (12, 1), (160, 1), (64, 1), (40, 1), (182, 1), (86, 1),
    (180, 1), (176, 1), (84, 1), (178, 1), (46, 1), (172, 1), (82, 1), (28, 1),
    (192, 1), (194, 1), (198, 1), (136, 1), (166, 1), (6, 1), (152, 1), (164, 1),
    (44, 1), (120, 1), (32, 1), (168, 1), (18, 1), (126, 1), (10, 1), (66, 1), (130, 1),
    (36, 1), (88, 1), (52, 1), (94, 1), (108, 1), (110, 1), (138, 1), (26, 1), (0, 1),
    (8, 1), (186, 1), (188, 1), (74, 1), (62, 1), (148, 1), (128, 1), (140, 1),
    (134, 1), (106, 1), (100, 1), (156, 1), (174, 1), (72, 1), (122, 1), (54, 1),
    (60, 1), (92, 1), (158, 1), (96, 1), (190, 1), (118, 1), (80, 1), (98, 1), (78, 1),
    (30, 1), (146, 1), (56, 1), (170, 1), (22, 1), (38, 1), (2, 1), (154, 1), (16, 1),
    (104, 1), (68, 1), (24, 1), (58, 1), (144, 1), (102, 1)
]
# fmt: on


class HintReplacementTest(TestCase):
    def test_do_hints_overlap_no(self) -> None:
        hints = [Hint(50, 20), Hint(30, 19), Hint(100, -21)]
        assert not do_hints_overlap(hints)

    def test_do_hints_overlap_yes(self) -> None:
        hints = [Hint(444, 63), Hint(0, 30), Hint(439, 62)]
        assert do_hints_overlap(hints)

    def test_do_hints_overlap_yes_touching(self) -> None:
        hints = [Hint(444, 63), Hint(400, 44), Hint(21, -21)]
        assert do_hints_overlap(hints)

    def test_do_hints_overlap_yes_touching_ghost(self) -> None:
        hints = [Hint(400, 79), Hint(300, 44), Hint(500, -21)]
        assert do_hints_overlap(hints)

    def test_do_hints_overlap_ghost(self) -> None:
        hints = [Hint(-14, 152), Hint(364, 146), Hint(730, -20), Hint(21, -21)]
        assert do_hints_overlap(hints)

    def test_do_hints_overlap_performance(self) -> None:
        hints = [Hint(pos, width) for pos, width in totally_random]
        start1 = time()
        assert do_hints_overlap(hints)
        stop1 = time()
        duration1 = (stop1 - start1) * 1000
        print(duration1)

    def test_do_hints_overlap_performance_no_overlap(self) -> None:
        hints = [Hint(pos, width) for pos, width in non_overlap]
        start1 = time()
        assert not do_hints_overlap(hints)
        stop1 = time()
        duration1 = (stop1 - start1) * 1000
        print(duration1)

    def test_charstring_hints_n(self) -> None:
        # BlueValues etc. are taken from the font
        fl_font = Font()
        fl_font.fake_set_master_blue_values(
            [-12, 0, 317, 325, 498, 510, 542, 554, 675, 687, 734, 746, 789, 797]
        )
        fl_font.fake_set_master_other_blues(
            [-258, -247, -182, -170, -130, -122, 187, 191, 343, 350]
        )
        fl_font.fake_set_master_stem_snap_h([46, 30])
        fl_font.fake_set_master_stem_snap_v([93])
        fl_glyph = Glyph()
        fl_glyph.fake_deserialize(G.Glyph, vfb_glyph)
        fl_font.glyphs.append(fl_glyph)
        autoreplace_glyph(fl_glyph)
        fl_font.Save("replacement_n_fakelab.vfb", save_json=True)
        result = [(r.type, r.index) for r in fl_glyph.replace_table]
        # TODO: Sort entries for better comparison, or build sets to compare
        assert result == [
            (1, 1),  # TYPE_HORIZONTAL_HINT
            (2, 1),  # TYPE_VERTICAL_HINT
            (1, 0),  # TYPE_HORIZONTAL_HINT
            (2, 0),  # TYPE_VERTICAL_HINT
            (TYPE_NODE, 7),
            (1, 2),  # TYPE_HORIZONTAL_HINT
            (2, 0),  # TYPE_VERTICAL_HINT
            (1, 1),  # TYPE_HORIZONTAL_HINT
            (2, 1),  # TYPE_VERTICAL_HINT
            (TYPE_NODE, 18),
            (1, 0),  # TYPE_HORIZONTAL_HINT
            (2, 1),  # TYPE_VERTICAL_HINT
            (1, 1),  # TYPE_HORIZONTAL_HINT
            (2, 0),  # TYPE_VERTICAL_HINT
        ]
