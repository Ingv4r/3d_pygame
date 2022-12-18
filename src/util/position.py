class Point2d:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y


class Position:
    def __init__(self, point: Point2d) -> None:
        self.point = point

    def update(self, x: float = 0, y: float = 0):
        self.point.x = x
        self.point.y = y
        return Position(Point2d(self.point.x, self.point.y))

    # todo: learn, how to override in python
    # def update(self, point: Point2d) -> None:
    #     self.point = point

    # ensure minus is working or write impl
