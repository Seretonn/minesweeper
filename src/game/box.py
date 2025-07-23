class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mine = False
        self.flag = False
        self.pajuo = False
        self.revealed = False
        self.adjacent_mines = 0
        self.adjacent_flags = 0

    def fresearse(self):
        self.pajuo = True

    def reveal(self):
        if not self.flag:
            self.revealed = True

    def put_flag(self):
        if not self.revealed:
            self.flag = True

    def remove_flag(self):
        self.flag = False

    def bury_mine(self):
        self.mine = True

    def __str__(self) -> str:
        if self.revealed:
            if self.mine:
                return "X"
            # Line for return a blank space (" ") instead of 0 when adjacent_mines is 0 ↴
            return str(self.adjacent_mines if self.adjacent_mines > 0 else " ") #       ←
        else:
            if self.flag:
                return "F"
            return "■"