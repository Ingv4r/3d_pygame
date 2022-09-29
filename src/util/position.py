from __future__ import annotations
from util.point2d import Point2d


class Position:
    def __init__(self, point: Point2d) -> None:
        self.point: Point2d = point

    def update(self, x: float = 0, y: float = 0) -> Position:
        self.point.x = x
        self.point.y = y
        return Position(Point2d(self.point.x, self.point.y))

    # todo: learn, how to override in python
    # def update(self, point: Point2d) -> None:
    #     self.point = point

    # ensure minus is working or write impl 
    def minus(self, position: Position) -> Position:
        self.point - position.point
