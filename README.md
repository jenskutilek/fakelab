# FakeLab

A FontLab Studio 5 replacement for testing Python code.

Everything is only implemented so far as to make FontLab objects importable
outside of FontLab Studio 5, and run tests.

It is suggested to install FakeLab in a virtual environment so FontLab won't
accidentally import the fake module when running the scripts in actual FontLab
Studio 5.

Saving VFBs is not supported, as the VFB format is not public, but you can save
`Font` objects as JSON.

The implementation of FakeLab is based on the invaluable
[Unofficial FontLab/Python API Reference](http://www.e-font.de/flpydoc/), and
from running scripts in FontLab Studio and checking what they do, apart from
crashing the application.

## Installation

When you have activated your virtual environment:

```bash
$ pip install -e .
```

FL is then importable outside of FontLab Studio:

```python
from FL import fl, Font

# Make an empty font
f = Font()

# Add the font to the mock app
fl.Add(f)

# Close the font
fl.Close()
```

## Writing tests

To be written
