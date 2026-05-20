from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int

    def __post_init__(self):
        if not isinstance(self.x, int):
            e = f"O parâmetro x precisa ser um int. ({type(self.x)})"
            raise TypeError(e)
        if not isinstance(self.y, int):
            e = f"O parâmetro y precisa ser um int. ({type(self.y)})"
            raise TypeError(e)

    @property
    def show(self) -> str:
        return f"({self.x}, {self.y})"


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    coord = Coordinate(x=1, y=2)

    print("\nCOORDINATE")
    print(coord)

    print("\nCOORDINATE.SHOW")
    print(coord.show)

    print(" END LOCAL TEST ".center(79, "="))
