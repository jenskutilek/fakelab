# fakelab tests/data/2axMM.vfb -s scripts/interpolate.py
from pathlib import Path

from FL import fl

f = fl.font
# print(f._axis_mappings_count, f._axis_mappings)
# print(f._primary_instance_locations)
# print(f._primary_instances)

base_path = Path(f.file_name).parent
# f.Save(str(base_path / "2axMM_roundtrip.vfb"))

instances = f.fake_generate_primary_instances()
for i in instances:
    filename = f"{i.pref_family_name}-{i.pref_style_name}.vfb"
    print(filename)
    i.Save(str(base_path / filename), save_json=True)
