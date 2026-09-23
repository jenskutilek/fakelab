from argparse import Namespace
from pathlib import Path

from FL.otfautohint.__main__ import HintOptions
from FL.otfautohint.autohint import FontInstance, fontWrapper, openFont

in_path = str(Path(__file__).parent / "replacement_n.ufo")

args = Namespace()
args.font_paths = [in_path]
args.output_paths = []
args.reference_font = None
args.reference_out = None
args.hint_all_ufo = True
args.allow_changes = True
args.no_flex = False
args.no_hint_sub = False
args.report_only = False
args.keep_conflicts = False
args.print_list_fddict = True
args.print_all_fddict = True
args.decimal = False
args.write_to_default_layer = True
args.max_segments = 100
args.verbose = True
args.loose_overlap_mapping = False
args.processes = 1
# FIXME
args.no_zones_stems = True
args.ignore_fontinfo = True
args.force_overlap = False
args.force_no_overlap = False

# Do the hinting
options = HintOptions(args)

fw = fontWrapper(options, [FontInstance(openFont(in_path, options), in_path, None)])
if fw.hint():
    fw.save()
