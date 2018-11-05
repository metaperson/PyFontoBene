class PyFontoBenePoint:
    def __init__(self, *, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y


class PyFontoBeneSize:
    def __init__(self, *, width: float, height: float) -> None:
        self.width: float = width
        self.height: float = height


class PyFontoBeneRect:
    def __init__(self, *, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
