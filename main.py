import os

class Game:
    def __init__(self):
        self.board = Board()

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

class Board:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.columns = cols
        # self.game_board = [[(row, column) for column in range(1, 10)] for row in range(1, 10)]
        self.game_board = [[Box(row, column) for column in range(cols)] for row in range(rows)]
        
        print("\nMinesweeper!\n")

        self.print_board()

    def print_board(self):
        for row in self.game_board:
            print(' | '.join(str(box) for box in row))
            if not (row == self.game_board[-1]):
                print(' | '.join("-" * (len(str(box))) for box in row))

    # OUTDATED
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

    def __str__(self) -> str:
        return "□"

class Pointer:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return ""

if __name__ == "__main__":
    game = Game()