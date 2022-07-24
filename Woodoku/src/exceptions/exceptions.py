class ShapeOutOfBoardError(Exception):
    """Exception raised for Error in placing a shape"""

    def __init__(self, x: int, y:int) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Cannot place shape at with top left corner at ({self.x}, {self.y})"
