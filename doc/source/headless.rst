Headless FontLab
================

FakeLab installs a `fakelab` command line script that allows running (something like)
FontLab Studio without GUI, and basically offers two different modes of operation.

This is the help for the `fakelab` command:

.. code-block:: text

    % fakelab -h
    usage: fakelab [-h] [-o OUT_PATH] [-d] [-r] [-s SCRIPT [SCRIPT ...]] [-v] [vfb ...]

    FontLab 5 external scripting

    positional arguments:
    vfb                   Path(s) to VFB file(s) to operate on. The last file will be the current font

    options:
    -h, --help            show this help message and exit
    -o, --out-path OUT_PATH
                            Save files to output path instead of overwriting the original files
    -d, --no-decompile    When roundtripping, don't decompile entries in JSON file
    -r, --roundtrip       Roundtrip specified VFB file(s) through FakeLab, then exit
    -s, --script SCRIPT [SCRIPT ...]
                            Path(s) to Python script(s) to run on the VFB file(s). The program exits after running the script(s)
    -v, --verbose         Verbose output


The `--no-decompile` and `--roundtrip` options are of limited utility, they can be used
for debugging, i.e. comparing the input and output files to see if the data is handled
correctly.


Running external Python scripts
-------------------------------

When one or more `-s/--script` arguments are present, `fakelab` is run in "script mode".
That means, any specified VFBs are opened, the Python script(s) at the path(s) are
loaded and executed, and the program exits.

.. note::

   I think I planned to auto-save the VFBs on exit, either overwriting the originals,
   or, when the `-o/--out-path` arguments are specified, saving them in that path. This
   is not implemented yet, so if you want to keep your changes, you need to save the
   VFBs yourself using `Font().Save(path_to_vfb)` on each modified font.


Interactive console
-------------------

If no external script is specified, the program runs as an interactive console. That
means, it opens the specified VFB file(s) (if any) and shows you a prompt that you can
use to interact with the app using Python commands.

When the `fakelab` package has been installed with the `repl` extra, or `ptpython` or
`ipython` is installed in the environment, they are used to improve the console
experience with autocompletion, history, and other niceties. If both are installed,
`ptpython` is preferred.

See `ptpython <https://github.com/prompt-toolkit/ptpython>`_ or 
`ipython <https://github.com/ipython/ipython>`_ for more information on those packages.


Limitations
-----------

Did I mention that only a small part of all FontLab Studio 5 Python API methods is
implemented? I plan to add them as needed, or you can help with that.


Generating fonts
~~~~~~~~~~~~~~~~

When FakeLab is installed with the `generate` extra, or the `ufo2ft` package is
installed in the Python environment, FakeLab can generate actual fonts.

This is achieved by converting the internal `Font` object to UFO(s) using the
`VfbToUfoBuilder` from `vfbLib`, and then generating binary fonts with `compileOTF` or
`compileTTF` from `ufo2ft`.

Note that those generated fonts won't be binary-compatible with those generated from the
actual FLS5.

*  FontLab's high-level TrueType commands are not compiled to TrueType bytecode, which
   `ufo2ft` would pick up
*  `ufo2ft` does not output PostScript hinting present in the UFO
*  Interpolation is not supported
*  OpenType layout features are compiled by `fontTools.feaLib` instead of the AFDKO.
