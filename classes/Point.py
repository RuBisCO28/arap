class Point():
    """ Point of Grid (i.e. embedding lattice) of the image """

    def __init__(self, x, y, w=1):
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :param w: weight
        """

        self._pos = [x, y]
        self._init = (x, y)  # intial state of point, doesn't need to be mutable
        self._linked = []
        self._link_cnt = 0
        self.weight = w

    @property
    def x(self):
        return self._pos[0]

    @property
    def ix(self):
        return self._init[0]

    @x.setter
    def x(self, value):
        self._pos[0] = value

    @property
    def y(self):
        return self._pos[1]

    @property
    def iy(self):
        return self._init[1]

    @y.setter
    def y(self, value):
        self._pos[1] = value

    def copy(self):
        return Point(self.x, self.y, self.weight)

    def link(self, other):
        """ Link another point """
        self._linked.append(other)
        self._link_cnt += 1

