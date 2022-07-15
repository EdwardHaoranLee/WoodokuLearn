from mimetypes import init


class CannotPlaceShapeError(Exception):
    """Exception raised for Error in placing a shape"""
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y


    def __str__(self) -> str:
        return f"Cannot place shape at coordinate ({self.x}, {self.y})"
    