import os
import random
from typing import Literal

class Game:
    def __init__(self):
        self.board = None
        self.difficulty = None

        # Reminder to update Game class attributes to dictionarie:
        # self.board = {
        #     "board": None, 
        #     "rows": 0, 
        #     "cols": 0,
        #     "style": None,
        #     "mines ratio": 0
        #     }

        self.playing = False
        self.is_running = False

    def run(self):
        self.is_running = True
        self.game_menu()

    def game_menu(self):
        while self.is_running:
            self.clear()
            
            print("Minesweeper!\n")

            choice = input("1. New game\n\n0. Quit\n\n> ")
            # removed instructions section
            # removed settings section

            match choice:
                case "1":
                    self.new_game()
                # case "2":
                #     self.intructions()
                # case "2":
                #     self.settings()
                case "0":
                    self.quit()
                case _:
                    self.pause("Invalid option. Try again")

    def new_game(self):
        self.playing = True

        self.difficulty = self.set_difficulty()

        if self.playing:
            self.board = Board(self.difficulty.get("mines ratio"), self.difficulty.get("rows"), self.difficulty.get("cols"))

        win = False
        lose = False
        box = None

        while self.playing:
            row = None
            col = None
            action = None
            
            self.clear()

            if win:
                print("Congratulations! You won!\n")
            elif lose:
                print("Game Over!\n")
            else:
                print("Minesweeper!\n")

                # print(f"Mines in board: {self.board.mines}\n")

            self.board.print_board(style="simple")

            if not win or not lose:
                self.board.check_adjacency(attribute="flag")

            if lose or win:
                self.pause("Press any key to go back to menu")
                self.stop_playing()
                break

            print("\nEnter 0 to exit the game")

            while True:
                operation = input("\nEnter the box row > ")
                
                try:
                    if int(operation) > 0 and int(operation) < self.board.rows + 1:
                        row = int(operation) - 1
                    elif int(operation) == 0:
                        self.stop_playing()
                        break
                    else:
                        self.pause("Invalid input. Try again!")
                        break
                except ValueError:
                    self.pause("Invalid input. Try again!")
                    break

                operation = input("\nEnter the column > ")
                
                try:
                    if int(operation) > 0 and int(operation) < self.board.cols + 1:
                        col = int(operation) - 1
                    elif int(operation) == 0:
                        self.stop_playing()
                        break
                    else:
                        self.pause("Invalid input. Try again!")
                        break
                except ValueError:
                    self.pause("Invalid input. Try again!")
                    break

                operation = input("\nEnter the action > ")
                
                match operation:
                    case "r" | "f":
                        action = operation
                    case "0":
                        self.stop_playing()
                        break
                    case _:
                        self.pause("Invalid input. Try again!")
                        break

                box = self.board.get_box(row, col)
                break

            if box:
                self.board.apply_act_to_box(box, action)

                # Check Win
                win = self.check_win()

                # Check Game Over
                lose = self.check_game_over()

    def set_difficulty(self):
        while self.playing:
            self.clear()

            print("Select difficulty:\n")
            print("1. begginer: 9x9 board, 12 mines") # ratio = 15%
            print("2. Intermediate: 16x16 board, 46 mines") # ratio = 18%
            print("3. Expert: 30x16 board, 101 mines\n") # ratio = 21%
            print("0. Exit\n")

            operation = input("> ")

            match operation:
                case "1":
                    difficulty = {
                        "level": "begginer",
                        "rows": 9,
                        "cols": 9,
                        "mines ratio": 15,
                    }
                case "2":
                    difficulty = {
                        "level": "intermediate",
                        "rows": 16,
                        "cols": 16,
                        "mines ratio": 18,
                    }
                case "3":
                    difficulty = {
                        "level": "expert",
                        "rows": 16,
                        "cols": 30,
                        "mines ratio": 21,
                    }
                case "0":
                    self.stop_playing()
                    break
                case _:
                    self.pause("Invalid input. Try again!")
                    continue
            
            return difficulty

    # OUTDATED
    def intructions(self):
        self.clear()
        print("Instructions:\n")
        print("Enter 1 to start a new game and display the grid on the screen")
        print("To interact with a box (put a flag, reveal, etc.) you must enter the coordinate of the box")
        print("To do that, you must follow the structure of the next example:\n")
        print("7,3,r\n")
        print("Where 7,3 are the coordinate (row 7, column 3) and \"r\" the action (reveal, could also be \"f\" for put flag)")
        self.pause()

    # INCOMPLETE
    def settings(self):
        self.setting_up = True
        pass

    def check_win(self):
        if self.board.flagged_mines == self.board.mines:
            self.pause("You have flagged all the mines!")
            self.board.reveal_all___(attribute="boxes")
            return True
        else:
            return False

    def check_game_over(self):
        for row in self.board.game_board:
            for box in row:
                if box.mine and box.revealed:
                    self.pause("You hit a mine!")
                    self.board.reveal_all___(attribute="mines")
                    return True
        return False

    def stop_playing(self):
        self.playing = False

    def quit(self):
        self.clear()
        print("Thanks for playing!")
        self.stop_playing()
        self.is_running = False

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self, text="Press any key to continue..."):
        if os.name == 'nt':
            if text is not None:
                print("\n" + text, end="")
            os.system('pause >nul')
        else:
            input(text)

class Board:
    def __init__(self, mines_ratio, rows=9, cols=9, board_style="simple"):
        self.rows = rows
        self.cols = cols
        self.flagged_mines = 0
        self.mines = self.calculate_mines(mines_ratio) # if mines == None else mines
        self.game_board = [[Box(row, column) for column in range(cols)] for row in range(rows)]

        self.bury_mines()
        self.check_adjacency(attribute="mine")

    def print_board(self, style: Literal["simple", "large"] = "simple"):
        match style:
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

    def calculate_mines(self, ratio):
        percentage = ratio/100
        mines = int(round((self.rows * self.cols) * percentage))
        return mines
    
    def bury_mines(self):
        mines_buried = 0
        while mines_buried < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.game_board[row][col].mine:
                self.game_board[row][col].bury_mine()
                mines_buried += 1

    def check_adjacency(self, attribute: Literal["mine", "flag"]):
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

    def reveal_all___(self, attribute: Literal["boxes", "mines"]):
        for row in self.game_board:
            for box in row:
                if attribute == "boxes":
                    box.reveal()
                else:
                    if box.mine:
                        box.reveal()

    def reveal_adjacent_boxes(self, selected_box):
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

    def add_to_flaggeds(self):
        self.flagged_mines += 1

    def subtract_from_flaggeds(self):
        self.flagged_mines -= 1

    def get_box(self, row, col):
        return self.game_board[row][col]

    def apply_act_to_box(self, box, act):
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
            else:
                # Line for return a blank space (" ") instead of 0 when adjacent_mines is 0 ↴
                return str(self.adjacent_mines if self.adjacent_mines > 0 else " ") #       ←
                
        elif not self.revealed and self.flag:
            return "F"
        elif not self.revealed:
            return "■"
        
class Pointer:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    game = Game()
    game.run()