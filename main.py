import os
import random

class Game:
    def __init__(self):
        self.board = Board()

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

class Board:
    def __init__(self, rows=9, cols=9):
        self.rows = rows
        self.cols = cols
        self.mines = self.calculate_mines()
        # self.game_board = [[(row, column) for column in range(1, 10)] for row in range(1, 10)]
        self.game_board = [[Box(row, column) for column in range(cols)] for row in range(rows)]
        
        print("\nMinesweeper!\n")

        self.print_board("simple")

    def print_board(self, style="fancy"):
        if style == "fancy":
            for row in self.game_board:
                print(' | '.join(str(box) for box in row))
                if not (row == self.game_board[-1]):
                    print(' | '.join("-" * (len(str(box))) for box in row))
        elif style == "simple":
            for row in self.game_board:
                for box in row:
                    if box == row[-1]:
                        print(str(box), end="\n")
                    else:
                        print(str(box), end=" | ")

    def calculate_mines(self):
        mines = int(round((self.rows * self.cols) * 0.2))
        return mines
    
    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            
            pass
        pass

    # OUTDATED - CURRENTLY USELESS
    def search_box(self, row, column):
        x = row - 1
        y = column - 1
        
        print(f"Value is {self.game_board[x][y]}")
        print(f"Row is {row} > {self.game_board[x]}")
        print(f"Column is ")
        for row in self.game_board:
            print("        " + str(row[2]))
        
class Box:
    def __init__(self, row, col):
        self.row = row
        self.column = col
        self.mine = None
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
        return "□"

class Pointer:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    game = Game()