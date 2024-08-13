import os
import random

class Game:
    def __init__(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        self.game_menu()

    def game_menu(self):
        while self.is_running:
            self.clear()
            
            self.title()

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
        current_game = True

        while current_game:
            self.clear()
            self.title()

            self.board.print_board(style="simple")

            operation = input("\nEnter the box coordinate and action:\n\n> ")
            
            # (7,3,r)

            if operation == "exit":
                current_game = False
                break
            else:
                self.board.search_box(operation.split(","))
    
    def title(self):
        print("Minesweeper!\n")

    def quit(self):
        self.clear()
        print("Thanks for playing!")
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
        self.mines = self.calculate_mines(ratio=21)
        self.game_board = [[Box(row, column) for column in range(cols)] for row in range(rows)]
        self.place_mines()
        self.count_adjacent_mines()

    def print_board(self, style="large"):
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
                self.game_board[row][col].put_mine()
                mines_placed += 1

    def count_adjacent_mines(self):
        for i, row in enumerate(self.game_board):
            for j, box in enumerate(row):
                count = 0

                # Legend:

                # tl = top left         t = top         tr = top right

                # l = left              center          r = right

                # bl = bottom left      b = bottom      br = bottom right

                # Statements:

                # 1. Top:
                t_box = self.game_board[i - 1][j].mine

                if j == 0:
                    tl_box = False
                else:
                    tl_box = self.game_board[i - 1][j - 1].mine

                try:
                    tr_box = self.game_board[i - 1][j + 1].mine
                except IndexError:
                    tr_box = False

                # 2. Center:
                if j == 0:
                    l_box = False
                else:
                    l_box = row[j - 1].mine

                try:
                    r_box = row[j + 1].mine
                except IndexError:
                    r_box = False

                # 3. Bottom:
                try:
                    b_box = self.game_board[i + 1][j].mine
                except IndexError:
                    b_box = False

                if i < self.rows - 1 and j > 0:
                    bl_box = self.game_board[i + 1][j - 1].mine
                else:
                    bl_box = False

                try:
                    br_box = self.game_board[i + 1][j + 1].mine
                except IndexError:
                    br_box = False
                
                # End of Statements

                if box.mine == False:

                    # Look for mines in top row
                    if not i == 0:
                        if t_box:
                            count += 1
                        if tl_box and tr_box:
                            count += 2
                        elif tl_box or tr_box:
                            count += 1
                    else: pass

                    # Look for mines in current row
                    if l_box and r_box:
                        count += 2
                    elif l_box or r_box:
                        count += 1

                    # Look for mines in bottom row
                    if not i == len(self.game_board) - 1:
                        if b_box:
                            count += 1
                        if bl_box and br_box:
                            count += 2
                        elif bl_box or br_box:
                            count += 1
                    else: pass
                else: continue

                box.adjacents_mines = count

    # OUTDATED - CURRENTLY USELESS:
    def search_box(self, data):
        row = int(data[0]) - 1
        col = int(data[1]) - 1
        act = data[2]
        
        box = self.game_board[row][col]

        print()

        if act == "r":
            box.reveal()
        else:
            box.put_flag()
        
        # print(f"Value is {self.game_board[x][y]}")
        # print(f"Row is {row} > {self.game_board[x]}")
        # print(f"Column is ")
        # for row in self.game_board:
        #     print("        " + str(row[2]))
        
class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.coord = (self.row, self.col)
        self.mine = False
        self.revealed = False
        self.flag = False
        self.adjacents_mines = None

    def reveal(self):
        self.revealed = True

    def put_flag(self):
        self.flag = True

    def remove_flag(self):
        self.flag = False

    def put_mine(self):
        self.mine = True

    def __str__(self) -> str:
        if self.revealed:
            if self.mine:
                return "⁕"
            else:
                return str(self.adjacents_mines)
        elif not self.revealed and self.flag:
            return "F"
        else:
            return "■"
        
class Pointer:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    game = Game()
    game.run()