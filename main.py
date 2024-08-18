import os
import random
from typing import Literal

class Game:
    def __init__(self):
        self.board = None
        self.playing = False
        self.is_running = False

    def run(self):
        self.is_running = True
        self.game_menu()

    def game_menu(self):
        while self.is_running:
            self.clear()
            
            print("Minesweeper!\n")

            choice = input("1. New game\n2. Instructions\n3. Quit\n\n> ")

            match choice:
                case "1":
                    self.new_game()
                    # break
                case "2":
                    self.clear()
                    print("Instructions:\n")
                    print("Enter 1 to start a new game and display the grid on the screen")
                    print("To interact with a box (put a flag, reveal, etc.) you must enter the coordinate of the box")
                    print("To do that, you must follow the structure of the next example:\n")
                    print("7,3,r\n")
                    print("Where 7,3 are the coordinate (row 7, column 3) and \"r\" the action (reveal, could also be \"f\" for put flag)")
                    self.pause()
                case "3":
                    self.quit()
                    # break
                case _:
                    self.pause("Invalid option. Try again")

    def new_game(self):
        self.board = Board()
        self.playing = True
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


            self.board.print_board(style="simple")
            self.board.check_adjacency(attribute="flag")

            if lose or win:
                self.pause("Press any key to go back to menu")
                self.stop_playing()
                break

            print("\nEnter 0 to exit the game")

            while True:
                operation = input("\nEnter the box row:\n\n> ")
                
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

                operation = input("\nEnter the column:\n\n> ")
                
                try:
                    if int(operation) > 0 and int(operation) < self.board.rows + 1:
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

                operation = input("\nEnter the action:\n\n> ")
                
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
                self.board.act_to_box(box, action)

                # Check Win
                win = self.check_win()

                # Check Game Over
                lose = self.check_game_over(box)

    def check_win(self):
        if self.board.flagged_mines == self.board.mines:
            return True
        else:
            return False

    def check_game_over(self, box):
        if box.mine and box.revealed:
            self.pause("You hit a mine!")
            self.board.reveal_all_mines()
            return True
        else:
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
    def __init__(self, rows=9, cols=9):
        self.rows = rows
        self.cols = cols
        self.flagged_mines = 0
        self.mines = self.calculate_mines(ratio=21)
        self.game_board = [[Box(row, column) for column in range(cols)] for row in range(rows)]

        self.place_mines()
        self.check_adjacency(attribute="mine")

    def print_board(self, style: Literal["simple", "large"] = "simple"):
        match style:
            case "large":
                for row in self.game_board:
                    if row == self.game_board[0]:
                        for n in range(len(row)):
                            print(f"{n + 1}" if not n == 0 else f"    {n + 1}", 
                                  end=" | " if not n == len(row) - 1 else "\n\n")
                            
                    print(self.game_board.index(row), end="   ")

                    print(' | '.join(str(box) for box in row))

                    if not (row == self.game_board[-1]):
                        print("-", end="   ")
                        print(' | '.join("-" * (len(str(box))) for box in row))

            case "simple":
                for row in self.game_board:
                    if row == self.game_board[0]:
                        for n in range(len(row)):
                            print(f"{n + 1}" if not n == 0 else f"    {n + 1}", end="   " if not n == len(row) - 1 else "\n\n")

                    print(self.game_board.index(row) + 1, end="   ")

                    for box in row:
                        if box == row[-1]:
                            print(str(box), end="\n")
                        else:
                            print(str(box), end=" | ")

    def calculate_mines(self, ratio):
        percentage = ratio/100
        mines = int(round((self.rows * self.cols) * percentage))
        return mines
    
    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.game_board[row][col].mine:
                self.game_board[row][col].bury_mine()
                mines_placed += 1

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

    def reveal_all_mines(self):
        for row in self.game_board:
            for box in row:
                if box.mine:
                    box.reveal()

    def reveal_adjacent_boxes(self, selected_box):
        for i, row in enumerate(self.game_board):
            for j, box in enumerate(row):
                if i == selected_box.row and j == selected_box.col:
                    # Legend:

                    # tl = top left         t = top         tr = top right

                    # l = left              box = center    r = right

                    # bl = bottom left      b = bottom      br = bottom right

                    # 1. Top row:
                    # --- Top center:
                    if i > 0:
                        t_box = self.game_board[i - 1][j]
                        t_box.reveal()

                        # --- Top left:
                        if j > 0:
                            tl_box = self.game_board[i - 1][j - 1]
                            tl_box.reveal()

                        # --- Top right:
                        if j < self.cols - 1:
                            tr_box = self.game_board[i - 1][j + 1]
                            tr_box.reveal()

                    # 2. Center row:
                    # --- Left
                    if j > 0:
                        l_box = row[j - 1]
                        l_box.reveal()

                    # --- Right
                    if j < self.cols - 1:
                        r_box = row[j + 1]
                        r_box.reveal()

                    # 3. Bottom:
                    # --- Bottom center
                    if i < self.rows - 1:
                        b_box = self.game_board[i + 1][j]
                        b_box.reveal()
                        
                        # --- Bottom left
                        if j > 0:
                            bl_box = self.game_board[i + 1][j - 1]
                            bl_box.reveal()

                        # --- Bottom right
                        if j < self.cols - 1:
                            br_box = self.game_board[i + 1][j + 1]
                            br_box.reveal()
                    break

    def add_to_flaggeds(self):
        self.flagged_mines += 1

    def subtract_from_flaggeds(self):
        self.flagged_mines -= 1

    def get_box(self, row, col):
        return self.game_board[row][col]

    def act_to_box(self, box, act):
        if act == "r":
            if (not box.mine and box.adjacent_mines == 0) or (box.adjacent_flags == box.adjacent_mines):
                self.reveal_adjacent_boxes(box)
            box.reveal()
        else:
            if not box.flag:
                box.put_flag()
                if box.mine and box.flag:
                    self.add_to_flaggeds()
            else:
                box.remove_flag()
                if box.mine and not box.flag:
                    self.subtract_from_flaggeds()
        
class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mine = False
        self.flag = False
        self.revealed = False
        self.adjacent_mines = 0
        self.adjacent_flags = 0

    def reveal(self):
        if self.flag:
            pass
        else:
            self.revealed = True

    def put_flag(self):
        self.flag = True

    def remove_flag(self):
        self.flag = False

    def bury_mine(self):
        self.mine = True

    def __str__(self) -> str:
        if self.revealed:
            if self.mine:
                return "⁕"
            else:
                return str(self.adjacent_mines)
                
                # Line for return a blank space (" ") instead of 0 when adjacent_mines is 0 ↴
                # return str(self.adjacent_mines if self.adjacent_mines > 0 else " ")       ←
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