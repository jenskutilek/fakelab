from FL.objects.Point import Point


class Component(object):
    def __init__(self, component_or_index=None, delta=None, scale=None):
        # Init with max num masters and -1 reference glyph
        self._deltas = [(0, 0)] * 16
        self._scales = [(1.0, 1.0)] * 16
        self._index = -1

        if isinstance(component_or_index, Component):
            # Copy constructor
            raise NotImplementedError

        elif isinstance(component_or_index, int):
            self._index = component_or_index
            if delta is not None:
                self.delta = delta
                if scale is not None:
                    self.scale = scale
        # else: Empty Component

    # Attributes

    @property
    def parent(self):
        """
        parent object, Glyph
        """
        raise NotImplementedError
        # return self._parent

    @property
    def index(self):
        """
        referencing glyph index
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def delta(self):
        """
        shift value
        """
        return self._deltas[0]

    @delta.setter
    def delta(self, value):
        assert isinstance(value, Point)
        self._deltas = [value] * len(self._deltas)

    @property
    def scale(self):
        """
        scale factor
        """
        return self._scales[0]

    @scale.setter
    def scale(self, value):
        assert isinstance(value, Point)
        self._scales = [value] * len(self._scales)

    @property
    def deltas(self):
        """
        list of shift values for each master
        """
        return self._deltas

    @property
    def scales(self):
        """
        list of scale values for each master
        """
        return self._scales

    # Methods

    def Get(self, f=None):
        """
        creates a glyph from component
        applying delta and scale transformations.
        Font parameter is not needed when component has a parent
        """
        raise NotImplementedError

    def Paste(self, f=None):
        """
        appends component to a parent glyph as a set of outlines.
        Component must have a parent
        """
        raise NotImplementedError
