

class Maze():
    def __init__(
            self, x1, y1,
            num_rows, num_cols, cell_size_x, cell_size_y, win, 
            ):
        self.x = x1
        self.y = y1
        self.rows = num_rows
        self.cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = [[Cell(x,y) for y in range(self.height)] for x in range(self.width)] 
        for columns in self._cells:
            for cell in column:
                self._draw_cell(cell)

    def _draw_cell(self, i, j):
        cell = Cell(win, i, j, cell_size_x, cell_size_y,
    def _animate(self):
