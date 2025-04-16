import random
import time

from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed=None,
        draw_now=True,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.seed = None if seed is None else random.seed(seed)
        self.draw_now = draw_now
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        if self.__num_rows <= 0:
            raise ValueError("Invalid number of rows given")
        if self.__num_cols <= 0:
            raise ValueError("Invalid number of columns given")
        if self.__cell_size_x <= 0:
            raise ValueError("Invalid horizontal cell size given")
        if self.__cell_size_y <= 0:
            raise ValueError("Invalid vertical cell size given")
        if self.__win is None:
            raise ValueError("Window is required")

        for n in range(self.__num_cols):
            curr_y1 = self.__y1 + n * self.__cell_size_y
            curr_y2 = self.__y1 + (n + 1) * self.__cell_size_y
            col_cells = []
            for m in range(self.__num_rows):
                curr_x1 = self.__x1 + m * self.__cell_size_x
                curr_x2 = self.__x1 + (m + 1) * self.__cell_size_x
                col_cells.append(Cell(curr_x1, curr_x2, curr_y1, curr_y2))
            self._cells.append(col_cells)

        if self.draw_now:
            for i in range(len(self._cells)):
                for j in range(len(self._cells[i])):
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.draw_now:
            cell_to_draw = self._cells[i][j]
            self.__win.draw_cell(cell_to_draw, "black")
            self._animate()

    def _animate(self):
        self.__win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False
        if self.draw_now:
            self._draw_cell(0, 0)
            self._draw_cell(-1, -1)

    def _break_walls_r(self, i, j):
        if (i == -1 or i == self.__num_rows - 1) and (
            j == -1 or j == self.__num_cols - 1
        ):
            return
        if (i == 0 and j == 0) and self._cells[i][j].visited:
            return
        self._cells[i][j].visited = True

        while True:
            waiting = []
            left = None
            right = None
            top = None
            bottom = None
            if i - 1 > 0:
                if not self._cells[i - 1][j].visited:
                    left = [i - 1, j]
                    waiting.append(left)
            if j - 1 > 0:
                if not self._cells[i][j - 1].visited:
                    top = [i, j - 1]
                    waiting.append(top)
            if i + 1 < len(self._cells):
                if not self._cells[i + 1][j].visited:
                    right = [i + 1, j]
                    waiting.append(right)
            if j + 1 < len(self._cells[i]):
                if not self._cells[i][j + 1].visited:
                    bottom = [i, j + 1]
                    waiting.append(bottom)
            if len(waiting) == 0:
                if self.draw_now:
                    self._draw_cell(i, j)
                return

            wall_index = random.randrange(0, len(waiting))
            x, y = waiting[wall_index]
            if [x, y] == top:
                self._cells[i][j].has_top_wall = False
                self._cells[x][y].has_bottom_wall = False
            elif [x, y] == bottom:
                self._cells[i][j].has_bottom_wall = False
                self._cells[x][y].has_top_wall = False
            elif [x, y] == right:
                self._cells[i][j].has_right_wall = False
                self._cells[x][y].has_left_wall = False
            elif [x, y] == left:
                self._cells[i][j].has_left_wall = False
                self._cells[x][y].has_right_wall = False

            if self.draw_now:
                self._draw_cell(i, j)
            self._break_walls_r(x, y)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        current = self._cells[i][j]

        if i == self.__num_rows - 1 and j == self.__num_cols - 1:
            return True

        if j < self.__num_rows - 1:
            bottom_cell = self._cells[i][j + 1]
            if not bottom_cell.visited:
                if not current.has_bottom_wall and not bottom_cell.has_top_wall:
                    is_solvable = self._solve_r(i, j + 1)
                    if is_solvable:
                        return True
                    else:
                        current.draw_move(
                            self.__win.get_canvas(), bottom_cell, undo=True
                        )

        if i < self.__num_cols - 1:
            right_cell = self._cells[i + 1][j]
            if not right_cell.visited:
                if not current.has_right_wall and not right_cell.has_left_wall:
                    is_solvable = self._solve_r(i + 1, j)
                    if is_solvable:
                        return True
                    else:
                        current.draw_move(
                            self.__win.get_canvas(), right_cell, undo=True
                        )

        if j - 1 > 0:
            top_cell = self._cells[i][j - 1]
            if not top_cell.visited:
                if not current.has_top_wall and not top_cell.has_bottom_wall:
                    is_solvable = self._solve_r(i, j - 1)
                    if is_solvable:
                        return True
                    else:
                        current.draw_move(self.__win.get_canvas(), top_cell, undo=True)

        if i - 1 > 0:
            left_cell = self._cells[i - 1][j]
            if not left_cell.visited:
                if not current.has_left_wall and not left_cell.has_right_wall:
                    is_solvable = self._solve_r(i - 1, j)
                    if is_solvable:
                        return True
                    else:
                        current.draw_move(self.__win.get_canvas(), left_cell, undo=True)

        return False
