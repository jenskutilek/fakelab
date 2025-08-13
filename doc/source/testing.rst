Testing FontLab Studio 5 macros
===============================

Test-driven development for FontLab Studio 5 Python macros and modules
----------------------------------------------------------------------

FakeLab is a FontLab Studio 5 replacement for testing Python code.

Everything is only implemented so far as to make FontLab objects importable
outside of FontLab Studio 5, and run tests.

Of course, nowadays you will run FakeLab in Python 3. You need to be aware that inside
FontLab Studio 5, your Python scripts and modules will run in Python 2. You must make
the scripts as future-proof as possible by importing the future:

.. code-block:: python

   from __future__ import absolute_import, print_function, unicode_literals

Still, it is easy to accidentally use Python-3-only language elements when developing
with FakeLab outside FLS5.

The ideal solution would be to run all your scripts outside FLS5 using FakeLab's
:doc:`headless` mode. This mode still needs lots of improvements, though.

The implementation of FakeLab is based on the invaluable
`Unofficial FontLab/Python API Reference <http://www.e-font.de/flpydoc>`_, and
from running scripts in FontLab Studio and checking what they do, apart from
crashing the application.

Installation
------------

When you have activated your virtual environment:

.. code-block:: bash

    $ pip install -e .

FL is then importable outside of FontLab Studio:

.. code-block:: python

    from FL import fl, Font

    # Make an empty font
    f = Font()

    # Add the font to the mock app
    fl.Add(f)

    # Close the font
    fl.Close()


If you are running in a virtual environment, and need to make your FontLab
modules importable, add a `.pth` file in your virtual environment's site-packages
directory:

.. code-block:: text

    # fl5modules.pth
    /Users/<yourname>/Code/FLMacros/System/Modules

A word of caution
-----------------

FakeLab is a work in progress, and only implemented as far as I needed it in my
own scripts. I have to admit that the bulk of them still has no tests.

If you encounter a `NotImplementedError` while writing tests, this is where you
can excel at helping to improve this project ;) I'll be happy to accept your
`pull requests <https://github.com/jenskutilek/fakelab/pulls>`_. Alternatively,
`open an issue <https://github.com/jenskutilek/fakelab/issues>`_.

Writing tests
-------------

Developing scripts without automated testing is really only for very small
projects. To be sure of the outcomes of a module or script, you should always
write tests. This is usually done using
`pytest <https://docs.pytest.org/en/stable/>`_.

Tests example
~~~~~~~~~~~~~

Let's assume you have a FontLab script to select glyphs containing components.
If you have your own tools collection for FontLab, this script may consist of
two parts: One script that is listed in FontLab's macro toolbar, and one Python
module implementing the logic, which is called by the toolbar script.

.. code-block:: text

   Studio 5
   +- Macros
   +- Selection
       +- Select Composites.py
   +- System
       +- Modules
           +- fakeLabDemo
               +- selection
               +- __init__.py
               +- composites.py


The `Select Composites.py` script looks like this:

.. code-block:: python

   #FLM: Select composites
   # Studio 5/Macros/Selection/Select Composites.py
   from fakeLabDemo.selection.composites import selectComposites
   selectComposites(fl.font)

And the module:

.. code-block:: python

    # Studio 5/Macros/System/Modules/fakeLabDemo/selection/composites.py
    from __future__ import absolute_import, division, print_function

    from FL import fl


    def getFontIndex(font):
        """
        Get the index of the supplied font.
        We must iterate through the open fonts and compare file names,
        because the == operator can not compare the font objects directly.
        (FL font objects get a different id() each time they are called)

        :param font: A title for the dialog.
        :type font:  :py:class:`FL.Font`
        """
        for i in range(len(fl)):
            cf = fl[i]
            if cf.file_name == font.file_name:
                if font.file_name is None:
                    if (
                        cf.family_name == font.family_name
                        and cf.style_name == font.style_name
                    ):
                        return (cf, i)
                else:
                    return (cf, i)
        # Font was not found, probably there are no open fonts
        return (None, -1)


    def setSelection(font, glyph_names):
        """
        Set glyphs from the glyph_names list as selected in the font window.
        """
        f, i = getFontIndex(font)
        if i > -1:
            fl.ifont = i
            fl.Unselect()
            for n in glyph_names:
                fl.Select(n)


    def selectComposites(font):
        """
        Select composites in font.
        """
        setSelection(
            font,
            [
                glyph.name
                for glyph in font.glyphs
                if glyph.components
            ]
        )

How can we be sure this script does what it is supposed to do? For pytest, we
add another parallel folder structure to the existing structure:

.. code-block:: text

   Studio 5
   +- Macros
   +- Selection
       +- Select Composites.py
   +- System
       +- Modules
           +- fakeLabDemo
               +- selection
               +- __init__.py
               +- composites.py
           +- tests
               +- fakeLabDemo
               +- selection
                   +- composites_test.py


The file `composites_test.py`, which is named analogous to the module file it
relates to, is where we will implement our tests:

.. code-block:: python

    # Studio 5/Macros/System/Modules/tests/fakeLabDemo/selection/composites_test.py
    import pytest

    from FL import fl, Component, Font, Glyph, Point
    from fakeLabDemo.selection.composites import selectComposites


    def test_selectComposites():
        # Construct a fake FontLab font object
        font = Font()
        g = Glyph(1)
        g.name = "A"
        g.width = 500
        g.unicode = 0x41
        font.glyphs.append(g)

        g = Glyph(1)
        g.name = "dieresis"
        g.width = 500
        g.unicode = 0xA8
        font.glyphs.append(g)

        g = Glyph(1)
        g.name = "Adieresis"
        g.width = 500
        g.unicode = 0xC4
        g.components.append(Component(0))
        g.components.append(Component(1, Point(0, 300)))
        font.glyphs.append(g)

        # Add the font to the FL object
        fl.Add(font)
        fl.UpdateFont()

        # Run our script to be tested on the font
        selectComposites(fl.font)

        # You could save the modified font to VFB for later inspection.
        # fl.font.Save("test_composites.vfb")

        # Test if the correct glyphs have been selected
        assert fl.Selected(0) == 0
        assert fl.Selected(1) == 0
        assert fl.Selected(2) == 1

        # Close the fake font
        fl.Close()

As you see, you can use the objects just as you would inside FontLab.

You can construct a minimal test font as shown in the example by using the
`FL Python API <http://www.e-font.de/flpydoc/>`_, or you can open an existing VFB file
with `Font().Open(path_to_vfb)`.

Invoke the test script in a Terminal window while your virtual environment is
active:

.. code-block:: bash

    cd "Studio 5/Macros/System/Modules"
    python -m pytest tests/fakeLabDemo/selection/composites_test.py


If everything works out, you will see some output like this:

.. code-block:: text

    ============================ test session starts ===============================
    platform darwin -- Python 3.8.7, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
    rootdir: /Users/<yourname>/Code/fakelab
    collected 1 item

    tests/fakeLabDemo/selection/composites_test.py .                          [100%]

    ============================= 1 passed in 0.02s ================================
