import tkinter as tk
from classes.CWrapper import CWrapper
from classes.ImageHelper import ImageHelper
from classes.Grid import Grid

class Application:
    def __init__(self, path):
        self._cw = CWrapper()
        
        self._window = tk.Tk()
        
        self._grid = None
        self._image = None
        self.load_image(path)
        
        self._canvas = tk.Canvas(self._window, width=self._image.width, height=self._image.height)
        self._canvas.pack()
        
        self._image.canvas = self._canvas
        
        self._active_handle = -1
        self._loop = None
        self._t_last = 0

    def load_image(self, path):
        self._image = ImageHelper(self._cw, path)

    def run(self):
        self._grid = Grid(self._cw, self._image)
        self._image.draw() # ImageHelper
        self._grid.draw() # Grid

        self._run_once()

        self._window.mainloop()

