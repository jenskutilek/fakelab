from __future__ import annotations

import argparse
from code import InteractiveConsole

from FL import fl

__startup_code__ = """
from FL import fl
"""


class FontLab5Console(InteractiveConsole):
    def __init__(self, startup_code: str = "", locals={}) -> None:
        namespace = locals
        # code = compile(__startup_code__, "", "exec", 0)
        # exec(code, namespace)
        super().__init__(locals=namespace)


def main():
    parser = argparse.ArgumentParser(description="FontLab 5 external scripting")
    parser.add_argument(
        "-o",
        "--out-path",
        type=str,
        nargs=1,
        help="Save files to output path instead of overwriting the original files",
    )
    parser.add_argument(
        "-s",
        "--script",
        type=str,
        nargs="+",
        help="Path(s) to Python scripts to run on the VFB file(s)",
    )
    parser.add_argument(
        "vfb",
        type=str,
        nargs="+",
        help=(
            "Path(s) to VFB file(s) to operate on. "
            "The last file will be the current font"
        ),
    )
    args = parser.parse_args()
    if args:
        for vfb_path in args.vfb:
            fl.Open(vfb_path, addtolist=True)
        if args.script:
            # If we have scripts, run them and exit.
            pass
        else:
            # Run the interactive console.
            console = FontLab5Console(locals={"fl": fl})
            console.interact(
                banner="Welcome to the FakeLab REPL.",
                exitmsg="Happy fonting, my friend!",
            )
    else:
        parser.print_help()
