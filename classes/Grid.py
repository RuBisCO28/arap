import math
from classes.Box import Box
from classes.Point import Point

class Grid:
    """
    Creates and manipulates grid of Boxes over the image,
    forces As Rigid As Possible image deformation
    via regularization and redraws the image
    """

    BOX_SIZE = 32
    CONTROL_WEIGHT = 100000

    iter = 0
    id = None

    def __init__(self, cw, image):

        self.visible = False

        self.cw = cw

        self._image = image
        self._points = {}
        self._boxes = []

        immask = self._image.mask

        # find borders of image
        top = self._border(immask)
        btm = self._image.height - self._border(immask[::-1])
        lft = self._border(immask.T)
        rgt = self._image.width - self._border(immask.T[::-1])

        width = rgt-lft
        height = btm-top

        box_count = (int(math.ceil(width/self.BOX_SIZE)), int(math.ceil(height/self.BOX_SIZE)))
        box_x = lft - int((box_count[0] * self.BOX_SIZE - width) / 2)
        box_y = top - int((box_count[1] * self.BOX_SIZE - height) / 2)

        # create Boxes over image
        for y in range(box_y, btm, self.BOX_SIZE):
            for x in range(box_x, rgt, self.BOX_SIZE):
                if -1 != self._border(immask[y:y+self.BOX_SIZE:1, x:x+self.BOX_SIZE:1]):
                    if x < 0 or x + self.BOX_SIZE > self._image.width \
                            or y < 0 or y + self.BOX_SIZE > self._image.height:
                        continue

                    self._boxes.append(
                        Box(
                            self.cw,
                            self._add_point(x, y),
                            self._add_point(x+self.BOX_SIZE, y),
                            self._add_point(x+self.BOX_SIZE, y+self.BOX_SIZE),
                            self._add_point(x, y+self.BOX_SIZE)
                        )
                    )

        """
        Control points setup
        key: Handle ID from ImageHelper
        item: [point ref, (x, y target coordinates), (x, y offset of grid Point from handle)]
        """
        self._controls = {}

    def _border(self, mask):
        """
        Finds the first row of the mask which contains foreground pixel.
        :return: row number in which the first foreground pixel was found, -1 if all pixels are empty
        """
        fg = 0
        stop = False
        for row in mask:
            i = 0
            for sign in row:
                if sign:
                    stop = True
                    break
                i += 1
            if stop:
                break
            fg += 1

        if not stop:
            return -1
        return fg

    def _add_point(self, x, y):
        """
        Creates new Point at given coordinate if it does not already exist
        :return: Point at given coordinates
        """
        if y in self._points:
            if x not in self._points[y]:
                self._points[y][x] = Point(x, y)
        else:
            self._points[y] = {}
            self._points[y][x] = Point(x, y)

        return self._points[y][x]

    def draw(self):
        """
        Visualize grid
        """
        self._image.canvas.delete("GRID")

        if self.visible:
            for box in self._boxes:
                box.draw(self._image.canvas, True)

