import time

class Maze():
    def __init__(
            self, x1, y1,
            num_rows, num_cols, cell_size_x, cell_size_y, win, 
            ):
        self.x1 = x1
        self.y1 = y1
        self.rows = num_rows
        self.cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = [[Cell(x,y) for y in range(self.rows)] for x in range(self.cols)] 
        for columns in self._cells:
            for cell in column:
                self._draw_cell(cell.x, cell.y)

    def _draw_cell(self, i, j):
        x_pos = self.x1 + (self.cell_size_x * i)
        y_pos = self.y1 + (self.cell_size_y * j)

        self._cells[i][j].draw(x_pos, y_pos)
        self._animate

    def _animate(self):
        win.redraw()
        time.sleep(0.05) 

