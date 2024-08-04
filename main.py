import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self) -> None:
        self.board = Board()

class Board:
    def __init__(self) -> None:
        self.game_board = [[(row, column) for column in range(1, 10)] for row in range(1, 10)]
        
        print("\nMinesweeper!\n")

        self.print_board()

    def print_board(self):
        for i, row in enumerate(self.game_board):
            print(f"{i + 1} > {row}")

    def search_box(self, row, column):
        x = row - 1
        y = column - 1
        
        print(f"Value is {self.game_board[x][y]}")
        print(f"Row is {row} > {self.game_board[x]}")
        print(f"Column is ")
        for row in self.game_board:
            print("        " + str(row[2]))
        

class Box:
    def __init__(self) -> None:
        self.mine = None

    def __str__(self) -> str:
        return "*"

if __name__ == "__main__":
    game = Game()