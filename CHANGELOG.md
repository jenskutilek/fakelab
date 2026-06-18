# Changelog

## v0.1.8

- Explicit exports in `FL/__init__.py` to make code checkers happy
- Update dependencies

## v0.1.7

- Fixes for `Font.DefineAxis()`
- Implement deleting glyphs (`del Font.glyphs[i]`)
- Add `Font.fake_open_from_vfblib(vfb)` to pass a Vfb object instead of opening a file

## v0.1.6

- Add some test files
- Fake a progress bar
- Implement a fake message dialog
- Don't insist on updating the font object if the index is out of range

## v0.1.5

- Update dependencies
- Remove future imports
- Adapt to vfbLib 0.11.2/3

## v0.1.4

- Add DirectionalList
- Use DirectionalList for hints and links in Glyph
- Improve Hint copy constructor
- Implement Hint.Transform()
- Point: Add type checks to match FL
- Point: Simpler copy constructor
- Node: use Assign, improve instantiation
- Implement Node.Transform()
- Matrix: Use Assign in constructor
- Implement Glyph.Decompose()

## v0.1.3

- Implement FL.output
- Font: Add properties relating to blue zones
- Font: Define/Remove axis
- TT Stem round keys are int now
- Font: Properties for ascender, descender, cap_height, x_height, default_width
- Add heuristic for axis names
- Fix Node instantiation for nCURVE, use ListParent, fix attr point
- Copy points when using adjust_list on a list of Point
- Prepare objects for adding/removal of axis
- Implement global mask de/serialization
- Font-level interpolation
- Point "rounding" uses floor
- Glyph-level interpolation
- Adapt to new vfbLib
- Print traceback when opening a VFB fails
- Get rid of previously unknown font entries
- Reader: Reflect VFB order
- Reader: Ignore block markers
- Implement reading ttinfo unknown fields
- Measurement line default is 300
- Implement unknown glyph fields
- Implement unknown gdef field
- Add Font.Save(save_json=True)
- Add weight_vector arg to GenerateInstance
- Improve Font: stem_snap, force_bold
- Interpolate guides, anchors, hints, kerning
- Always depend on vfbLib
- Remove fake_vfb_object, fake_binary
- Fix hint instantiation
- Don't care about the kern pair order for now
- Fix image serde
- Node: handle "open path" flag
- Clean up class handling
- Fix afm export
- Raise minimum Python to 3.11, streamline testing

## v0.1.2

- Change reader/writer API
- Improve documentation
- Implement `ForSelected`
- Fix circular import
- Persist FL options
- Set vendor code from Options in empty font
- Keep existing spaces in glyph classes
- Restore Python 3.10 compatibility

## v0.1.1

- Bug fixes, test fixes

## v0.1.0

- First published version
