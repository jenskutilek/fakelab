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
        """
        The interactive console. You usually don't use this class directly; it is
        started by the `main` function in this module, which is available on the command
        line via the `fakelab` command.

        Args:
            startup_code (str, optional): Currently ignored. Defaults to "".
            locals (dict[str, Any] | None, optional): Additional locals. Defaults to None.
        """
        namespace = locals or {}
        # code = compile(__startup_code__, "", "exec", 0)
        # exec(code, namespace)
        super().__init__(locals=namespace)


def main() -> None:
    """
    Run the `fakelab` commandline script.

    If one or more Python files are specified in the `---script` argument, those scripts
    are executed and the program exits.

    If no external script is specified, the program runs as an interactive console.

    Run `fakelab -h` to see a description of all command line arguments.

    When fakelab has been installed with the `repl` extra, or `ptpython` or `ipython` is
    installed in the environment, it is used to improve the console experience with
    autocompletion, history, and other niceties. If both are installed, `ptpython` is
    preferred.
    See `ptpython <https://github.com/prompt-toolkit/ptpython>`_ or
    `ipython <https://github.com/ipython/ipython>`_ for details.
    """
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
        help=(
            "Path(s) to Python script(s) to run on the VFB file(s). "
            "The program exits after running the script(s)"
        ),
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
                # FIXME: Did we plan to autosave the VFBs respecting the -o argument? (#11)
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
