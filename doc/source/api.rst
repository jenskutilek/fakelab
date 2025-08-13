API
===

Naming conventions
------------------

Methods and attributes that start with `fake` are additions not present in the original
FontLab Studio 5 Python API. They are used here for additional functionality.

In most cases, those methods have been added to the main object in `FL.objects`, but if
more additions are necessary, they may have been moved to a base class in `FL.fake`.

Modules
-------

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   FL.fake
   FL.helpers
   FL.objects
   FL.vfb
   FL.cmdline
   FL.constants
   FL.fl_cmd
   FL.FLdict