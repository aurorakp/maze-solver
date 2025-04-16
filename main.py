from maze import Maze
from window import Window


def main():
    win = Window(800, 600)
    m = Maze(100, 200, 4, 5, 30, 30, win)
    m._break_walls_r(0, 0)
    m._reset_cells_visited()
    s = m.solve()
    print(f"solvable? {s}")
    win.wait_for_close()


if __name__ == "__main__":
    main()
