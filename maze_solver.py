from tkinter import Tk, BOTH, Canvas 

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("My Window")
        self.root.geometry(f"{width}x{height}")
        self.canvas = Canvas(self.root, width = width, height = height)
        self.canvas.pack()
        self.running = False 
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, Line, fill_color):
        Line.draw(self.canvas,fill_color)

class Point():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(
                self.start.x, self.start.y, self.end.x, self.end.y, fill = fill_color, width = 2
                )

class Cell():
    def __init__(
            self, window, top_x, top_y, bottom_x, bottom_y, 
            top_wall = True, right_wall = True, bottom_wall = True, left_wall =True 
            ):
        self.has_left_wall = left_wall
        self.has_right_wall = right_wall
        self.has_top_wall = top_wall
        self.has_bottom_wall = bottom_wall
        self._x1 = top_x
        self._x2 = bottom_x
        self._y1 = top_y
        self._y2 = bottom_y
        self._win = window

    def draw(self):
        fill = "black"
        if self.has_top_wall:
            P1 = Point(self._x1, self._y1)
            P2 = Point(self._x2, self._y1)
            L1 = Line(P1, P2)
            L1.draw(self._win.canvas, fill)
        if self.has_right_wall:
            P3 = Point(self._x2, self._y1)
            P4 = Point(self._x2, self._y2)
            L2 = Line(P3, P4)
            L2.draw(self._win.canvas, fill)
        if self.has_bottom_wall:
            P5 = Point(self._x2, self._y2)
            P6 = Point(self._x1, self._y2)
            L3 = Line(P5, P6)
            L3.draw(self._win.canvas, fill)
        if self.has_left_wall:
            P7 = Point(self._x1, self._y1)
            P8 = Point(self._x1, self._y2)
            L4 = Line(P7, P8)
            L4.draw(self._win.canvas, fill)

    def draw_move(self, to_cell, undo):
        if undo == False:
            fill = "red"
        else:
            fill = "gray"
        P1 = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        P2 = Point((to_cell._x1 + to_cell._x2) /2 , (to_cell._y1 + to_cell._y2) / 2)
        L1 = Line(P1, P2) 
        L1.draw(self._win.canvas, fill)
        



def main():
    win = Window(800,600)
    c1 = Cell(win, 200, 200, 300, 300, True, True, True, True)
    c1.draw()
    c2 = Cell(win, 200, 300, 300, 400, True , True, True, True)
    c2.draw()

    

if __name__ ==  "__main__":
    main()
