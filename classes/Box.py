import numpy as np
import math
from classes.Point import Point

class Box():
    """ Represents one box in a grid layed over image"""

    def __init__(self, cw, b_tl, b_tr, b_br, b_bl):
        """
        :param cw: CWrapper object
        :param b_tl: top-left point of a box
        :param b_tr: top-right point of a box
        :param b_br: bottom-right point of a box
        :param b_bl: bottom-left point of a box
        """

        self._cw = cw
        self.boundary = [b_tl, b_tr, b_br, b_bl]

        # box fitted into boundaries
        self._rigid = [b_tl.copy(), b_tr.copy(), b_br.copy(), b_bl.copy()]

        self.boundary[0].link(self._rigid[0])
        self.boundary[1].link(self._rigid[1])
        self.boundary[2].link(self._rigid[2])
        self.boundary[3].link(self._rigid[3])

        # homography matrices
        self.H = None

        H_A = []
        H_B = [None]*8
        for s in self._rigid:
            H_A.append([s.ix, s.iy, 1, 0, 0, 0, None, None])
            H_A.append([0, 0, 0, s.ix, s.iy, 1, None, None])

        self.H_A = np.array(H_A)
        self.H_B = np.array(H_B)

        # centroids cache
        self._qc = Point(0, 0)  # target centroid
        self._pc = Point(0, 0)  # source centroid, same during whole object live
        self.compute_source_centroid()

    def compute_source_centroid(self):
        w = self.boundary[0].weight + self.boundary[1].weight + self.boundary[2].weight + self.boundary[3].weight
        self._pc.x = (self.boundary[0].weight * self._rigid[0].ix
                      + self.boundary[1].weight * self._rigid[1].ix
                      + self.boundary[2].weight * self._rigid[2].ix
                      + self.boundary[3].weight * self._rigid[3].ix) / w
        self._pc.y = (self.boundary[0].weight * self._rigid[0].iy
                      + self.boundary[1].weight * self._rigid[1].iy
                      + self.boundary[2].weight * self._rigid[2].iy
                      + self.boundary[3].weight * self._rigid[3].iy) / w

