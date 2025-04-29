import unittest
from solver import *

class Test(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10 
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10) 
        self.assertEqual(
            len(m1._cells), 
            num_cols, 
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows, 
        )

    def test_maze_create_cells_2(self):
        num_cols = 30
        num_rows = 14 
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10) 
        self.assertEqual(
            len(m1._cells), 
            num_cols, 
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows, 
        )

    def test_maze_create_cells_3(self):
        num_cols = 12
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10) 
        self.assertEqual(
            len(m1._cells), 
            num_cols, 
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows, 
        )

    def test_maze_create_cells_4(self):
        num_cols = 75
        num_rows = 45
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10) 
        self.assertEqual(
            len(m1._cells), 
            num_cols, 
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows, 
        )
        

    def test_entrance_(self):
        num_cols = 3
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10) 
        self.assertFalse(
            m1._cells[0][0].has_top_wall, 
        )
        self.assertFalse(
            m1._cells[-1][-1].has_bottom_wall,
        )
        
if __name__ == "__main__":
    unittest.main()

