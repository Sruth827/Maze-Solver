from tkinter import Tk, BOTH, Canvas 

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title = ("My Window")
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

def main():
    win = Window(800,600)
    p1 = Point()
    p2 = Point(180, 200)
    l1 = Line(p1, p2)
    win.draw_line(l1, "#FF0000")
    p3 = Point(400, 400)
    p4 = Point(700, 700)
    l2 = Line(p3,p4)
    win.draw_line(l2, "#FFF000")
    win.wait_for_close()


if __name__ ==  "__main__":
    main()
