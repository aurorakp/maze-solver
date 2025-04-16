import unittest
import unittest.mock

from maze import Maze
from window import Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win, seed=None, draw_now=False)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    @unittest.mock.patch.object(Maze, "_draw_cell")
    def test_maze_create_cells__animate(self, mocked_draw):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertTrue(mocked_draw.called)

    def test_maze_needs_rows(self):
        with self.assertRaisesRegex(ValueError, "Invalid number of rows given"):
            win = Window(800, 600)
            Maze(0, 0, 0, 5, 10, 10, win, seed=None, draw_now=False)

    def test_maze_needs_cols(self):
        with self.assertRaisesRegex(ValueError, "Invalid number of columns given"):
            win = Window(800, 600)
            Maze(0, 0, 5, 0, 10, 10, win, seed=None, draw_now=False)

    def test_maze_needs_width(self):
        with self.assertRaisesRegex(ValueError, "Invalid horizontal cell size given"):
            win = Window(800, 600)
            Maze(0, 0, 5, 5, 0, 10, win, seed=None, draw_now=False)

    def test_maze_needs_length(self):
        with self.assertRaisesRegex(ValueError, "Invalid vertical cell size given"):
            win = Window(800, 600)
            Maze(0, 0, 5, 5, 10, 0, win, seed=None, draw_now=False)

    def test_maze_needs_window(self):
        with self.assertRaisesRegex(ValueError, "Window is required"):
            Maze(0, 0, 5, 5, 10, 10, None, seed=None, draw_now=False)

    def test_maze_has_entrance_and_exit(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win, seed=None, draw_now=False)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[-1][-1].has_bottom_wall)

    def test_maze_visited_can_be_reset(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win, seed=None, draw_now=False)
        m1._break_walls_r(0, 0)
        self.assertTrue(m1._cells[0][0].visited)
        m1._reset_cells_visited()
        for i in range(12):
            for j in range(10):
                self.assertFalse(m1._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()
