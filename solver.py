import time
import random
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
            self, top_x, top_y, bottom_x, bottom_y, 
            top_wall = True, right_wall = True, bottom_wall = True, left_wall =True, window = None 
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
        self.visited = False

    def draw(self):
        if self._win is None:
            return 
        fill_1 = "black"
        fill_2 = "white"
        if self.has_top_wall:
            P1 = Point(self._x1, self._y1)
            P2 = Point(self._x2, self._y1)
            L1 = Line(P1, P2)
            L1.draw(self._win.canvas, fill_1)
        if self.has_top_wall == False:
            P1 = Point(self._x1, self._y1)
            P2 = Point(self._x2, self._y1)
            L1 = Line(P1, P2)
            L1.draw(self._win.canvas, fill_2)

        if self.has_right_wall:
            P3 = Point(self._x2, self._y1)
            P4 = Point(self._x2, self._y2)
            L2 = Line(P3, P4)
            L2.draw(self._win.canvas, fill_1)
        if self.has_right_wall == False:
            P3 = Point(self._x2, self._y1)
            P4 = Point(self._x2, self._y2)
            L2 = Line(P3, P4)
            L2.draw(self._win.canvas, fill_2)
       

        if self.has_bottom_wall:
            P5 = Point(self._x2, self._y2)
            P6 = Point(self._x1, self._y2)
            L3 = Line(P5, P6)
            L3.draw(self._win.canvas, fill_1)
        if self.has_bottom_wall == False:
            P5 = Point(self._x2, self._y2)
            P6 = Point(self._x1, self._y2)
            L3 = Line(P5, P6)
            L3.draw(self._win.canvas, fill_2)   
        
        if self.has_left_wall:
            P7 = Point(self._x1, self._y1)
            P8 = Point(self._x1, self._y2)
            L4 = Line(P7, P8)
            L4.draw(self._win.canvas, fill_1)
        if self.has_left_wall == False:
            P7 = Point(self._x1, self._y1)
            P8 = Point(self._x1, self._y2)
            L4 = Line(P7, P8)
            L4.draw(self._win.canvas, fill_2)


    def draw_move(self, to_cell, undo = False):
        if undo == False:
            fill = "red"
        else:
            fill = "white"
        P1 = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        P2 = Point((to_cell._x1 + to_cell._x2) /2 , (to_cell._y1 + to_cell._y2) / 2)
        L1 = Line(P1, P2) 
        L1.draw(self._win.canvas, fill)
        



class Maze():
    def __init__(
            self, x1, y1,
            num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None
            ):
        self.x1 = x1
        self.y1 = y1
        self.rows = num_rows
        self.cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self.seed = seed
        if self.seed != None: #will be used for random maze generation
            random.seed(seed)

    def _create_cells(self):
        self._cells = []
        for i in range(self.cols):
            column = []
            for j in range(self.rows):
                top_x = self.x1 + (i * self.cell_size_x)
                top_y = self.y1 + (j * self.cell_size_y)
                bottom_x = top_x + self.cell_size_x
                bottom_y = top_y + self.cell_size_y
                cell = Cell(top_x, top_y, bottom_x, bottom_y, window = self.win)
                column.append(cell)
                print(f"create cell at {top_x} , {top_y}")
            self._cells.append(column)

        for i in range(self.cols):
            for j in range(self.rows):
                self._draw_cell(i, j)
        
        #call function to establist path and create entrance and exit 
        #functions found below
        self._break_walls_r(0, 0)
        self._break_entrance_and_exit()
        #reset all cells.visited to false to then allow for pathfinding
        self._reset_cells_visited()

    #included print statement to ensure 2D array is handled correctly 
    def _draw_cell(self, i, j):
        print(f"drawing at {i},{j}")
        cell = self._cells[i][j]
        if self.win == None: 
            return
        cell.draw()
        if self.win:
            self._animate()

    #time delay used to show proper drawing of maze cells prior to walls breaking for path
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05) 

    #remove walls for entrance(top left) to exit(bottom right)
    def _break_entrance_and_exit(self):
        start_cell = self._cells[0][0]
        start_cell.has_top_wall = False
        start_cell.draw() 
        end_cell = self._cells[-1][-1]
        end_cell.has_bottom_wall = False
        end_cell.draw()

    
    
    #Recurisive Depth First Search used to create path through maze
    #One possible path from entrance(top left) to exit(bottom right)
    def _break_walls_r(self, i, j):
        cur = self._cells[i][j]
        cur.visited = True
        while True:
            need_to_visit=[]

            #find any unvisited neighbors and add to list
            #had i and j backwards, now fixed to properly account for maze boundaries
            directions = [(0,1), (1,0), (0,-1), (-1,0)]
            for dirx, diry in directions:
                ni, nj = i + diry, j + dirx
                if 0 <= ni < self.cols and 0 <= nj < self.rows and not self._cells[ni][nj].visited:                 need_to_visit.append((dirx, diry, ni, nj))
        
            #if no unvisited neights, draw current node
            if not need_to_visit:
                cur.draw()
                return        

            next = random.choice(need_to_visit)
            dirx, diry, ni, nj = next 
            if (dirx, diry) == (0, 1):
                cur.has_right_wall = False 
                next_cell = self._cells[ni][nj]
                next_cell.has_left_wall = False
            elif (dirx, diry) == (1, 0):
                cur.has_bottom_wall = False
                next_cell = self._cells[ni][nj]
                next_cell.has_top_wall = False
            elif (dirx, diry) == (0, -1):
                cur.has_left_wall = False 
                next_cell = self._cells[ni][nj]
                next_cell.has_right_wall = False
            elif (dirx, diry) == (-1, 0):
                cur.has_top_wall = False 
                next_cell = self._cells[ni][nj]
                next_cell.has_bottom_wall = False
            cur.draw()
            next_cell.draw()
            
            #recursive call
            self._break_walls_r(ni, nj)




    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
                print(f"cell visited {cell.visited}")
            
                
    def solve(self):
        self._solve_r(0, 0)
        

    def _solve_r(self, i, j):
        self._animate()
        cur = self._cells[i][j]
        cur.visited = True
        if cur == self._cells[-1][-1]:
            return True
        directions = [(0,1, "has_right_wall"), (1,0, "has_bottom_wall"), (0,-1, "has_left_wall"), (-1,0, "has_top_wall")]

        for dirx, diry, wallattr in directions:
            ni, nj = i + diry, j + dirx
            if 0 <= ni < self.cols and 0 <= nj < self.rows:
                next_cell = self._cells[ni][nj]
                if not next_cell.visited and not getattr(cur, wallattr):
                    cur.draw_move(next_cell)
                                         
                    if self._solve_r(ni, nj):
                        return True
            
        return False




def main():
    win = Window(1080, 1080)

    maze = Maze(20, 20, 19, 19, 50, 50, win)
    maze.solve()
    win.wait_for_close()

    

if __name__ ==  "__main__":
    main()
