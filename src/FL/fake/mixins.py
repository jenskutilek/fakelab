from __future__ import annotations

import logging

from vfbLib.typing import GuidePropertiesDict, GuidePropertyDict, MMGuidesDict

from FL.objects.Guide import Guide

logger = logging.getLogger(__name__)


class GuideMixin:
    def fake_deserialize_guides(self, data: MMGuidesDict) -> None:
        for k, target in (("h", self.hguides), ("v", self.vguides)):
            if dir_master_guides := data[k]:
                for guide_dict in dir_master_guides:
                    g = Guide(guide_dict[0]["pos"], guide_dict[0]["angle"])
                    for master_index in range(1, self._masters_count):
                        g._positions[master_index] = guide_dict[master_index]["pos"]
                        g._widths[master_index] = Guide.fake_angle_to_width(
                            guide_dict[master_index]["angle"]
                        )
                    target.append(g)

    def fake_serialize_guides(self) -> MMGuidesDict:
        mgd = MMGuidesDict(h=[], v=[])
        for direction, source in (("h", self.hguides), ("v", self.vguides)):
            for guide in source:
                guide_masters = []
                for master_index in range(self._masters_count):
                    guide_masters.append(
                        {
                            "pos": guide.positions[master_index],
                            "angle": Guide.fake_width_to_angle(
                                guide.widths[master_index]
                            ),
                        }
                    )
                mgd[direction].append(guide_masters)
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
