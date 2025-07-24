from .config import EMPTY, MINE, FLAG, BOX

class Box:
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col
        self.mine: bool = False
        self.flag: bool = False
        self.pajuo: bool = False
        self.revealed: bool = False
        self.adjacent_mines: int = 0
        self.adjacent_flags: int = 0

    def fresearse(self) -> None:
        self.pajuo = True

    def reveal(self) -> None:
        if not self.flag:
            self.revealed = True

    def put_flag(self) -> None:
        if not self.revealed:
            self.flag = True

    def remove_flag(self) -> None:
        self.flag = False

    def bury_mine(self) -> None:
        self.mine = True

    def __str__(self) -> str:
        if self.revealed:
            if self.mine:
                return MINE
            # Line for returning a blank space (" ") instead of 0 when adjacent_mines is 0 ↴
            return str(self.adjacent_mines if self.adjacent_mines > 0 else EMPTY) #       ←
        else:
            if self.flag:
                return FLAG
            return BOX