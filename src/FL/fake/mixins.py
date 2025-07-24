from __future__ import annotations

import logging

from vfbLib.typing import GuidePropertiesDict, GuidePropertyDict, MMGuidesDict

from FL.objects.Guide import Guide

logger = logging.getLogger(__name__)


class GuideMixin:
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
                        guide = target[guide_index]
                        guide._positions[master_index] = guide_dict["pos"]
                        guide._widths[master_index] = Guide.fake_angle_to_width(
                            guide_dict["angle"]
                        )

    def fake_serialize_guides(self) -> MMGuidesDict:
        mgd = MMGuidesDict()
        mgd["h"] = [[] for _ in range(self._masters_count)]
        mgd["v"] = [[] for _ in range(self._masters_count)]
        for direction, source in (("h", self.hguides), ("v", self.vguides)):
            for master_index in range(self._masters_count):
                for guide in source:
                    mgd[direction][master_index].append(
                        {
                            "pos": guide.positions[master_index],
                            "angle": Guide.fake_width_to_angle(
                                guide.widths[master_index]
                            ),
                        }
                    )
        return mgd


class GuidePropertiesMixin:
    def fake_deserialize_guide_properties(self, data: GuidePropertiesDict) -> None:
        for k, target in (("h", self.hguides), ("v", self.vguides)):
            num_guides = len(target)
            for guide_prop_dict in data[k]:
                guide_index = guide_prop_dict["index"] - 1
                if guide_index >= num_guides:
                    logger.info(
                        "Skipping properties for guide that isn't present: "
                        f"{guide_index} in {target}"
                    )
                    continue

                color = guide_prop_dict.get("color")
                if color:
                    target[guide_index]._color = color
                name = guide_prop_dict.get("name")
                if name:
                    target[guide_index]._name = name

    def fake_serialize_guide_properties(self) -> GuidePropertiesDict:
        gpl = GuidePropertiesDict(h=[], v=[])
        for k, target in (("h", self.hguides), ("v", self.vguides)):
            for i, guide in enumerate(target):
                d = GuidePropertyDict(index=i + 1)
                if guide._color:
                    d["color"] = guide._color
                if guide._name:
                    d["name"] = guide._name
                if "color" in d or "name" in d:
                    gpl[k].append(d)
        return gpl
