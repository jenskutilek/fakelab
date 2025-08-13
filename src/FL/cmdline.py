from __future__ import annotations

import argparse
import logging
from code import InteractiveConsole
from pathlib import Path
from typing import Any

from vfbLib.json import save_vfb_json

from FL import environment, fl

try:
    from ptpython.repl import embed

    have_ptpython = True
except ImportError:
    have_ptpython = False

try:
    from IPython import embed as iembed

    have_ipython = True
except ImportError:
    have_ipython = False


__doc__ = """
The interactive console
"""


logger = logging.getLogger(__name__)


__startup_code__ = """
from FL import fl
"""


class FontLab5Console(InteractiveConsole):
    def __init__(
        self, startup_code: str = "", locals: dict[str, Any] | None = None
    ) -> None:
        namespace = locals or {}
        # code = compile(__startup_code__, "", "exec", 0)
        # exec(code, namespace)
        super().__init__(locals=namespace)


def main() -> None:
    parser = argparse.ArgumentParser(description="FontLab 5 external scripting")
    parser.add_argument(
        "-o",
        "--out-path",
        type=str,
        nargs=1,
        help="Save files to output path instead of overwriting the original files",
    )
    parser.add_argument(
        "-d",
        "--no-decompile",
        action="store_true",
        default=False,
        help="When roundtripping, don't decompile entries in JSON file",
    )
    parser.add_argument(
        "-r",
        "--roundtrip",
        action="store_true",
        default=False,
        help="Roundtrip specified VFB file(s) through FakeLab, then exit",
    )
    parser.add_argument(
        "-s",
        "--script",
        type=str,
        nargs="+",
        help="Path(s) to Python scripts to run on the VFB file(s)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Verbose output",
    )
    parser.add_argument(
        "vfb",
        type=str,
        nargs="*",
        help=(
            "Path(s) to VFB file(s) to operate on. "
            "The last file will be the current font"
        ),
    )
    args = parser.parse_args()
    if args:
        if args.verbose:
            logging.basicConfig(level=logging.INFO)
        if args.roundtrip:
            for vfb_path in args.vfb:
                logger.info(vfb_path)
                fl.Open(vfb_path, addtolist=False)
                out_path = Path(vfb_path).with_suffix(".fake.vfb")
                fl.Save(str(out_path))
                save_vfb_json(out_path, no_decompile=args.no_decompile)
        else:
            for vfb_path in args.vfb:
                logger.info(vfb_path)
                fl.Open(vfb_path, addtolist=True)
            if args.script:
                # If we have scripts, run them and exit.
                for script_path in args.script:
                    exec(Path(script_path).read_text(), locals=environment)
            else:
                # Run the interactive console.
                if have_ptpython:
                    # globals=globals()?
                    embed(locals=environment, vi_mode=True)
                elif have_ipython:
                    iembed(globals=globals(), locals=environment, header="FakeLab")
                else:
                    console = FontLab5Console(locals=environment)
                    console.interact(
                        banner="Welcome to the Headless FakeLab REPL.",
                        exitmsg="Happy fonting, my friend!",
                    )
    else:
        parser.print_help()
