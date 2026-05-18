from dataclasses import dataclass


@dataclass
class Coordenate:
    x: int
    y: int

    def __post_init__(self):
        if not isinstance(self.x, int):
            erro_msg = f"O parâmetro x precisa ser um int. ({type(self.x)})"
            raise TypeError(erro_msg)
        if not isinstance(self.y, int):
            erro_msg = f"O parâmetro y precisa ser um int. ({type(self.y)})"
            raise TypeError(erro_msg)


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    coord = Coordenate(x=1, y=2)
    print(coord)
    print(" END LOCAL TEST ".center(79, "="))
