from point import Point
from line import Line


class Cell:
    def __init__(
        self,
        x1,
        x2,
        y1,
        y2,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
        visited=False,
    ):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited = visited

    def draw(self, canvas, fill_color):
        if canvas is None:
            return

        top_left = Point(self.__x1, self.__y1)
        lower_left = Point(self.__x1, self.__y2)
        top_right = Point(self.__x2, self.__y1)
        lower_right = Point(self.__x2, self.__y2)
        left_wall = Line(top_left, lower_left)
        right_wall = Line(top_right, lower_right)
        top_wall = Line(top_left, top_right)
        bottom_wall = Line(lower_left, lower_right)
        if self.has_left_wall:
            left_wall.draw(canvas, fill_color)
        else:
            left_wall.draw(canvas, "white")
        if self.has_right_wall:
            right_wall.draw(canvas, fill_color)
        else:
            right_wall.draw(canvas, "white")
        if self.has_top_wall:
            top_wall.draw(canvas, fill_color)
        else:
            top_wall.draw(canvas, "white")

        if self.has_bottom_wall:
            bottom_wall.draw(canvas, fill_color)
        else:
            bottom_wall.draw(canvas, "white")

    def draw_move(self, canvas, to_cell, undo=False):
        track_color = "red"
        if undo:
            track_color = "gray"

        self_mid = Point(
            self.__x1 + (abs(self.__x2 - self.__x1) / 2),
            self.__y1 + (abs(self.__y2 - self.__y1) / 2),
        )
        to_mid = Point(
            to_cell.__x1 + (abs(to_cell.__x2 - to_cell.__x1) / 2),
            to_cell.__y1 + (abs(to_cell.__y2 - to_cell.__y1) / 2),
        )
        track_line = Line(self_mid, to_mid)
        track_line.draw(canvas, track_color)

    def __repr__(self):
        return f"Cell: top left: {self.__x1}, {self.__y1}, top right: {self.__x2}, {self.__y2}, \n \
        walls: left: {self.has_left_wall},  right: {self.has_right_wall}, top: {self.has_top_wall}, bottom: {self.has_bottom_wall}"

    def get_coords(self):
        return [self.__x1, self.__y1, self.__x2, self.__y2]
