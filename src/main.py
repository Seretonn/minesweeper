import os
from typing import Optional

import game.config as config
from game.board import Board

class Game:
    def __init__(self) -> None:
        self.playing: bool = False
        self.is_running: bool = False
        self.difficulty: Optional[dict] = None
        self.board: Optional[Board] = None

    def start_playing(self) -> None:
        self.playing = True

    def stop_playing(self) -> None:
        self.playing = False

    def run(self) -> None:
        self.is_running = True
        self.game_menu()

    def stop_running(self) -> None:
        self.is_running = False

    def game_menu(self) -> None:
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
        self.start_playing()

        self.difficulty = self.set_difficulty()

        if not self.difficulty:
            self.stop_playing()
            return

        self.board = Board(
            rows = self.difficulty.get("rows", config.DEFAULT_ROWS),
            cols = self.difficulty.get("cols", config.DEFAULT_COLS), 
            mines_ratio = self.difficulty.get("mines ratio", config.DEFAULT_MINES_RATIO)
        )

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

            self.board.print_board()

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

            if box and action:
                self.board.apply_act_to_box(box, action)

                # Check Win
                win = self.check_win()

                # Check Game Over
                lose = self.check_game_over()

    def set_difficulty(self) -> Optional[dict]:
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
                    return config.DIFFICULTIES["begginer"]
                case "2":
                    return config.DIFFICULTIES["intermediate"]
                case "3":
                    return config.DIFFICULTIES["expert"]
                case "0":
                    self.stop_playing()
                    break
                case _:
                    self.pause("Invalid input. Try again!")
                    continue

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
        # Calembe linter que me obliga a poner esta validacion nojoda
        if not self.board:
            return False        
        if self.board.flagged_mines == self.board.mines:
            self.pause("You have flagged all the mines!")
            self.board.reveal_all___(attribute="boxes")
            return True
        else:
            return False

    def check_game_over(self):
        # Y aqui tambien, linter der coño
        if not self.board:
            return False
        for row in self.board.game_board:
            for box in row:
                if box.mine and box.revealed:
                    self.pause("You hit a mine!")
                    self.board.reveal_all___(attribute="mines")
                    return True
        return False

    def quit(self):
        self.clear()
        print("Thanks for playing!")
        self.stop_playing()
        self.stop_running()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self, text="Press any key to continue..."):
        if os.name == 'nt':
            if text is not None:
                print("\n" + text, end="")
            os.system('pause >nul')
        else:
            input(text)

if __name__ == "__main__":
    game = Game()
    game.run()