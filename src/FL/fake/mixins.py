from vfbLib.typing import GuidePropertiesDict, MMGuidesDict

from FL.objects.Guide import Guide


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
                        target[guide_index].position.append(guide_dict["pos"])
                        target[guide_index].angle.append(guide_dict["angle"])

    def fake_serialize_guides(self) -> MMGuidesDict:
        mgd = MMGuidesDict(h=[], v=[])
        return mgd


class GuidePropertiesMixin:
    def fake_deserialize_guide_properties(self, data: GuidePropertiesDict) -> None:
        for k, target in (("h", self.hguides), ("v", self.vguides)):
            for guide_prop_dict in data[k]:
                guide_index = guide_prop_dict["index"] - 1
                color = guide_prop_dict.get("color")
                if color:
                    target[guide_index]._color = color
                name = guide_prop_dict.get("name")
                if name:
                    target[guide_index]._name = name

    def fake_serialize_guide_properties(self) -> GuidePropertiesDict:
        gpl = GuidePropertiesDict(h=[], v=[])
        return gpl
