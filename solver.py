import sys
import traceback
import time
import random
import psutil
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from collections import deque

class Window:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("Algorithm Visualization")
        self.root.geometry(f"{width}x{height}")
        self.canvas = tk.Canvas(self.root, width = width, height = height)
        self.canvas.place(x = 0, y = 0)
        self.console = tk.Text(self.root, wrap = "word", height = 10, width = 50)
        self.console.pack()
        self.console.place(x = 700, y = 100, width = 300, height = 890)
        self.running = False 
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas.create_text(700, 80, text = "Traceback Stack", anchor = W,font = ("Ubuntu" , 18), fill = "Black" )
        self.canvas.create_text(50, 30, text = "Depth-First Search", anchor = W,font = ("Ubuntu" , 18), fill = "Black" )
        self.canvas.create_text(50, 380, text = "Breadth-First Search",anchor = W, font = ("Ubuntu", 18), fill = "Black" )
        self.canvas.create_text(50, 730, text = "BFS with reconstruct",anchor = W, font = ("Ubuntu", 18),  fill = "Black")
        self.canvas.lower(self.root)


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
    
   
    def log_stack(self):
        stack = traceback.extract_stack()  
        recursive_calls = []

        seen_functions = set()
        for frame in stack:
            func_name = frame.name
            if func_name in seen_functions:  
                recursive_calls.append(f"Line: {frame.lineno} | Recursive Call {frame.line} - {func_name}")
            seen_functions.add(func_name)

        if recursive_calls:
            stack_info = "\n".join(recursive_calls)
        else:
            stack_info = "No recursive calls detected."

        self.console.insert(tk.END, stack_info + "\n\n")  
        self.console.see(tk.END)  

    def get_memory_usage(self):
       process = psutil.Process(os.getpid())
       return process.memory_info().rss
    
    def update_memory_canvas(self, mem_usage, x, y, maze_name):
       
        text_id = f"mem_{maze_name}"  

        self.canvas.delete(text_id) 
        self.canvas.create_text(x, y, text=f"{maze_name} Memory:\n{mem_usage} bytes",font=("Ubuntu", 14), anchor = W, fill="Black", tags=text_id)

class Point():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y




class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        return canvas.create_line(
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
        self.drawn_lines = []
        self.visited = False
        self.color = None

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
            fill = "blue"
        P1 = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        P2 = Point((to_cell._x1 + to_cell._x2) /2 , (to_cell._y1 + to_cell._y2) / 2)
        L1 = Line(P1, P2) 
        lineID = L1.draw(self._win.canvas, fill)
        self.drawn_lines.append(lineID)

    def clear_move(self):
        for lineID in self.drawn_lines:
            self._win.canvas.delete(lineID)
        self.drawn_lines.clear()
    
    def highlight(self):
        self.color = (0, 255, 0)
        self.draw()

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
        

    #time delay used to show proper drawing of maze cells prior to walls breaking for path
    def _animate(self, speed):
        self.win.redraw()
        time.sleep(speed) 

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
        self.win.log_stack()
        cur = self._cells[i][j]
        cur.visited = True
        while True:
            self._animate(0.02)
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
            
                
    def solveDFS(self):
        self._solve_DFS(0, 0)
        

    def _solve_DFS(self, i, j):
        self.win.log_stack()
        self._animate(0.05)
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
                                         
                    if self._solve_DFS(ni, nj):
                        return True
            
        return False
    
    
    def solve_BFS(self):
        self.win.log_stack()
        queue = deque([(0,0)])

        while queue:
            i, j = queue.popleft()
            self._animate(0.05) 
            cur = self._cells[i][j]
            cur.visited = True
            if cur == self._cells[-1][-1]:
                return True
            directions = [(0,1, "has_right_wall"), (1,0, "has_bottom_wall"), (0,-1, "has_left_wall"), (-1,0, "has_top_wall")]

            for dirx, diry, wallattr in directions:
                ni, nj  = i + diry, j + dirx
                if 0 <= ni < self.cols and 0 <= nj < self.rows:
                    next_cell = self._cells[ni][nj]
                    if not next_cell.visited and not getattr(cur, wallattr):
                        cur.draw_move(next_cell)
                        queue.append((ni, nj))
                        next_cell.visited = True
        return False


    def solve_BFS_with_helper(self):
        self.win.log_stack()
        queue = deque([(0, 0)])
        parent_map = {}  # Track predecessors for reconstructing the path

        while queue:
            i, j = queue.popleft()
            self._animate(0.05)
            cur = self._cells[i][j]
            cur.visited = True

            if cur == self._cells[-1][-1]:  # Goal reached, reconstruct path
                return self._reconstruct_path(parent_map, i, j)

            directions = [(0,1, "has_right_wall"), (1,0, "has_bottom_wall"),
                          (0,-1, "has_left_wall"), (-1,0, "has_top_wall")]

            for dirx, diry, wallattr in directions:
                ni, nj = i + diry, j + dirx
                if 0 <= ni < self.cols and 0 <= nj < self.rows:
                    next_cell = self._cells[ni][nj]
                
                    if not next_cell.visited and not getattr(cur, wallattr):
                        cur.draw_move(next_cell)
                        queue.append((ni, nj))
                        next_cell.visited = True  # Mark as visited here
                        parent_map[(ni, nj)] = (i, j)  # Store parent for path tracing

        return False  # No solution found

    def _reconstruct_path(self, parent_map, i, j):
        #Backtracks from goal to reconstruct the single path
        path = []
        while (i, j) in parent_map:
            path.append((i, j))
            i, j = parent_map[(i, j)]
         
        path.reverse()  # Reverse to start from the beginning
        
        for x, y in path:
            self._cells[x][y].clear_move()

        for index in range(len(path) -1):
            x1, y1 = path[index]
            x2, y2 = path[index + 1]
            self._cells[x1][y1].draw_move(self._cells[x2][y2], True)
                                           


def main():
    win = Window(1080, 1080)
    
    mazeDFS = Maze(30, 50, 20, 20, 15, 15, win)
    mazeBFS = Maze (30, 400, 20, 20, 15, 15, win)
    mazeBFShelper = Maze (30, 750, 20, 20, 15, 15, win)

    before_dfs = win.get_memory_usage()
    win.update_memory_canvas(before_dfs, x = 350, y = 70, maze_name = "Before solveDFS()")
    mazeDFS.solveDFS()
    after_dfs = win.get_memory_usage()
    dfs_mem_used = after_dfs - before_dfs
    print(f"Before DFS : {before_dfs}")
    print(f"DFS Mem Usage: {after_dfs - before_dfs} bytes")
    win.update_memory_canvas(after_dfs, x = 350, y = 150, maze_name = "After solveDFS()")
    win.update_memory_canvas(dfs_mem_used, x = 350, y = 230, maze_name = "solveDFS() Used")

    before_bfs = win.get_memory_usage()
    win.update_memory_canvas(before_bfs, x = 350, y = 420, maze_name = "Before solve_BFS()")    
    mazeBFS.solve_BFS()
    after_bfs = win.get_memory_usage()
    bfs_mem_used = after_bfs - before_bfs
    print(f"Before BFS : {before_bfs}")
    print(f"BFS Mem Usage: {after_bfs - before_bfs} bytes")
    win.update_memory_canvas(after_bfs, x = 350, y = 500, maze_name = "After solve_BFS()")   
    win.update_memory_canvas(bfs_mem_used, x = 350, y = 580, maze_name = "solve_BFS() Used")   

    before_bfs_helper = win.get_memory_usage()
    win.update_memory_canvas(before_bfs_helper, x = 350, y = 770, maze_name = "Before solve_BFS_with_helper()")    
    mazeBFShelper.solve_BFS_with_helper()
    after_bfs_helper = win.get_memory_usage()
    bfs_helper_mem_used = after_bfs_helper - before_bfs_helper
    print(f"Before BFS_helper : {before_bfs_helper}")
    print(f"BFS with Reconstruct Mem Usage: {after_bfs_helper - before_bfs_helper} bytes")
    win.update_memory_canvas(after_bfs_helper, x = 350, y = 850, maze_name = "After solve_BFS_with_helper()")
    win.update_memory_canvas(bfs_helper_mem_used, x = 350, y = 930, maze_name = "solve_BFS_with_helper() Used")

    win.wait_for_close()

    

if __name__ ==  "__main__":
    main()
