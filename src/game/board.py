import random
from typing import Literal

from .box import Box
from . import config

class Board:
    def __init__(
            self, 
            rows: int = config.DEFAULT_ROWS, 
            cols: int = config.DEFAULT_COLS, 
            mines_ratio: int = config.DEFAULT_MINES_RATIO, 
            board_style: str = config.DEFAULT_STYLE
            ) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.flagged_mines: int = 0
        self.mines: int = self.calculate_mines(mines_ratio) # if mines == None else mines
        self.game_board: list[list[Box]] = [[Box(row, column) for column in range(cols)] for row in range(rows)]

        self.bury_mines()
        self.check_adjacency(attribute="mine")

    def print_board(self, style: Literal["simple", "large"] = "simple") -> None:
        match style:
            case "simple":
                for i, row in enumerate(self.game_board):
                    if row == self.game_board[0]:
                        for n in range(len(row)):
                            print(f"{n + 1}" if not n == 0 else f"     {n + 1}", end="   " if (n + 1) < 10 else "  ") # if not n == len(row) - 1 else "\n\n")
                        print()
                        print()
                
                    print(f" {i + 1}" if (i + 1) < 10 else f"{i + 1}", end="   ")

                    for box in row:
                        if box == row[-1]:
                            print(str(box), end="\n")
                        else:
                            print(str(box), end=" | ")

            case "large":
                for row in self.game_board:
                    if row == self.game_board[0]:
                        for n in range(len(row)):
                            print(f"{n + 1}" if not n == 0 else f"    {n + 1}", end=" | " if not n == len(row) - 1 else "\n\n")
                            
                    print(self.game_board.index(row), end="   ")

                    print(' | '.join(str(box) for box in row))

                    if not (row == self.game_board[-1]):
                        print("-", end="   ")
                        print(' | '.join("-" * (len(str(box))) for box in row))

    def calculate_mines(self, ratio: int) -> int:
        mines, percentage = 0, 0
        percentage = ratio/100
        mines = int(round((self.rows * self.cols) * percentage))
        return mines
    
    def bury_mines(self) -> None:
        mines_buried = 0
        while mines_buried < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.game_board[row][col].mine:
                self.game_board[row][col].bury_mine()
                mines_buried += 1

    def check_adjacency(self, attribute: Literal["mine", "flag"]) -> None:
        for i, row in enumerate(self.game_board):
            for j, box in enumerate(row):
                count = 0
                
                # Legend:

                # tl = top left         t = top         tr = top right

                # l = left              center          r = right

                # bl = bottom left      b = bottom      br = bottom right

                # Statements:

                # 1. Top row:
                # --- Top center:
                if i > 0:
                    t_box = getattr(self.game_board[i - 1][j], attribute)
                    if t_box:
                        count += 1

                    # --- Top left:
                    if j > 0:
                        tl_box = getattr(self.game_board[i - 1][j - 1], attribute)
                        if tl_box:
                            count += 1

                    # --- Top right:
                    if j < self.cols - 1:
                        tr_box = getattr(self.game_board[i - 1][j + 1], attribute)
                        if tr_box:
                            count += 1

                # 2. Center row:
                # --- Left
                if j > 0:
                    l_box = getattr(row[j - 1], attribute)
                    if l_box:
                        count += 1

                # --- Right
                if j < self.cols - 1:
                    r_box = getattr(row[j + 1], attribute)
                    if r_box:
                        count += 1

                # 3. Bottom:
                # --- Bottom center
                if i < self.rows - 1:
                    b_box = getattr(self.game_board[i + 1][j], attribute)
                    if b_box:
                        count += 1
                    
                    # --- Bottom left
                    if j > 0:
                        bl_box = getattr(self.game_board[i + 1][j - 1], attribute)
                        if bl_box:
                            count += 1

                    # --- Bottom right
                    if j < self.cols - 1:
                        br_box = getattr(self.game_board[i + 1][j + 1], attribute)
                        if br_box:
                            count += 1

                if attribute == "mine":
                    box.adjacent_mines = count
                else:
                    box.adjacent_flags = count

    def reveal_all___(self, attribute: Literal["boxes", "mines"]) -> None:
        for row in self.game_board:
            for box in row:
                if attribute == "boxes":
                    box.reveal()
                else:
                    if box.mine:
                        box.reveal()

    def reveal_adjacent_boxes(self, selected_box: Box) -> None:
        if selected_box.adjacent_mines == 0:
            selected_box.fresearse()
        for i, row in enumerate(self.game_board):
            for j, box in enumerate(row):
                if box == selected_box:
                    # Legend:

                    # tl = top left         t = top         tr = top right

                    # l = left              box = center    r = right

                    # bl = bottom left      b = bottom      br = bottom right

                    # 1. Top row:
                    # --- Top center
                    if i > 0:
                        t_box = self.game_board[i - 1][j]

                        # Considera que, si box.adjacent_mines == 0:
                            # self.apply_act_to_box(t_box, "r")

                        if selected_box.pajuo or t_box.adjacent_mines == 0:
                            self.apply_act_to_box(t_box, "r")
                        else:
                            t_box.reveal()

                        # --- Top left
                        if j > 0:
                            tl_box = self.game_board[i - 1][j - 1]
                            if selected_box.pajuo or tl_box.adjacent_mines == 0:
                                self.apply_act_to_box(tl_box, "r")
                            else:
                                tl_box.reveal()

                        # --- Top right
                        if j < self.cols - 1:
                            tr_box = self.game_board[i - 1][j + 1]
                            if selected_box.pajuo or tr_box.adjacent_mines == 0:
                                self.apply_act_to_box(tr_box, "r")
                            else:
                                tr_box.reveal()

                    # 2. Center row:
                    # --- Left
                    if j > 0:
                        l_box = row[j - 1]
                        if selected_box.pajuo or l_box.adjacent_mines == 0:
                            self.apply_act_to_box(l_box, "r")
                        else:
                            l_box.reveal()

                    # --- Right
                    if j < self.cols - 1:
                        r_box = row[j + 1]
                        if selected_box.pajuo or r_box.adjacent_mines == 0:
                            self.apply_act_to_box(r_box, "r")
                        else:
                            r_box.reveal()

                    # 3. Bottom row:
                    # --- Bottom center
                    if i < self.rows - 1:
                        b_box = self.game_board[i + 1][j]
                        if selected_box.pajuo or b_box.adjacent_mines == 0:
                            self.apply_act_to_box(b_box, "r")
                        else:
                            b_box.reveal()
                        
                        # --- Bottom left
                        if j > 0:
                            bl_box = self.game_board[i + 1][j - 1]
                            if selected_box.pajuo or bl_box.adjacent_mines == 0:
                                self.apply_act_to_box(bl_box, "r")
                            else:
                                bl_box.reveal()

                        # --- Bottom right
                        if j < self.cols - 1:
                            br_box = self.game_board[i + 1][j + 1]
                            if selected_box.pajuo or br_box.adjacent_mines == 0:
                                self.apply_act_to_box(br_box, "r")
                            else:
                                br_box.reveal()
                    break

    def add_to_flaggeds(self) -> None:
        self.flagged_mines += 1

    def subtract_from_flaggeds(self) -> None:
        self.flagged_mines -= 1

    def get_box(self, row: int, col: int) -> Box:
        return self.game_board[row][col]

    def apply_act_to_box(self, box: Box, act: str) -> None:
        if act == "r":
            if not box.pajuo:
                if not box.mine:
                    if (box.adjacent_mines == 0) or (box.revealed and box.adjacent_flags == box.adjacent_mines):
                        self.reveal_adjacent_boxes(box)
                box.reveal()
        elif act == "f":
            if not box.flag:
                box.put_flag()
                if box.mine and box.flag:
                    self.add_to_flaggeds()
            else:
                box.remove_flag()
                if box.mine and not box.flag:
                    self.subtract_from_flaggeds()
        else: 
            pass