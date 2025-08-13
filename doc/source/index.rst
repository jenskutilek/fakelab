Welcome to FakeLab's documentation!
===================================

FakeLab is an independent reimplementation of the FontLab Studio 5 Python API.

It can be used to run automated tests of internal macros outside FontLab Studio 5, or to
run Python scripts on VFB files outside FontLab Studio 5 ("headless FontLab").

.. note::

   This project is under active development. Expect road bumps and potholes.
   
   All objects of the FLS5 Python API are only implemented so far as to make FontLab
   objects importable outside the app. Some methods are implemented to actually do the
   same as they do in FontLab Studio 5. Of course, I hope that this will expand in the
   future. Even the functionality that is there is in no way guaranteed to be 100%
   compatible to the actual app, or to have the same results.


Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   testing
   headless
   api


Further reading
---------------

* The VFB file format is described in https://github.com/jenskutilek/vfbLib-rust/blob/main/FILEFORMAT.md
* The FontLab Studio 5 TrueType hinting is described in https://github.com/jenskutilek/fakelab/blob/main/doc/truetype-hinting/index.md

Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`