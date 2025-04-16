from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Maze"
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(master=self.__root)
        self.__canvas.configure(background="white")
        self.__canvas.pack(expand="true", fill=BOTH)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self.__canvas, fill_color)

    def draw_cell_move(self, cell1, cell2, undo=False):
        cell1.draw_move(self.__canvas, cell2, undo=undo)

    def get_canvas(self):
        return self.__canvas
