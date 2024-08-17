import os
import random

class Game:
    def __init__(self):
        self.box = False
        self.board = None
        self.playing = False
        self.is_running = False

    def run(self):
        self.is_running = True
        self.game_menu()

    def game_menu(self):
        while self.is_running:
            self.clear()
            
            self.show_title()

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

        while self.playing:
            row = None
            col = None
            action = None
            
            self.clear()

            if win:
                print("Congratulations! You won!\n")
            elif lose:
                self.show_game_over()
            else:
                self.show_title()

            self.board.print_board(style="simple")

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

                self.box = self.board.get_box(row, col)
                break

            if self.box:
                self.board.act_to_box(self.box, action)

                # Check Win
                win = self.check_win()

                # Check Game Over
                lose = self.check_game_over()

    def show_title(self):
        print("Minesweeper!\n")

    def check_win(self):
        if self.board.flagged_mines == self.board.mines:
            return True
        else:
            return False

    def check_game_over(self):
        if self.box.mine and self.box.revealed:
            self.board.reveal_all_mines()
            self.pause("You hit a mine!")
            return True
        else:
            return False

    def show_game_over(self):
        print("Game Over!\n")

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
        self.count_adjacent_mines()

    def print_board(self, style="simple"):
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

                box.adjacent_mines = count

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

                    # Statements:

                    # 1. Top row:
                    # --- Top center:
                    # if not i == 0:
                    if i > 0:
                        t_box = self.game_board[i - 1][j]
                        t_box.reveal()

                        # --- Top left:
                        if j > 0:
                        # if not j == 0:
                            tl_box = self.game_board[i - 1][j - 1]
                            tl_box.reveal()

                        # --- Top right:
                        if j < self.cols - 1:
                        # if not j == self.cols - 1:
                            tr_box = self.game_board[i - 1][j + 1]
                            tr_box.reveal()

                    # try:
                    #     tr_box = self.game_board[i - 1][j + 1]
                    #     tr_box.reveal()
                    # except IndexError:
                    #     tr_box = False

                    # 2. Center row:
                    # --- Left
                    if j > 0:
                        l_box = row[j - 1]
                        l_box.reveal()

                    # --- Right
                    if j < self.cols - 1:
                        r_box = row[j + 1]
                        r_box.reveal()

                    # try:
                    #     r_box = row[j + 1]
                    #     r_box.reveal()
                    # except IndexError:
                    #     r_box = False

                    # 3. Bottom:
                    # --- Bottom center
                    if i < self.rows - 1:
                    # if not i == self.rows - 1:
                        b_box = self.game_board[i + 1][j]
                        b_box.reveal()
                        
                        # --- Bottom left
                        if j > 0:
                            bl_box = self.game_board[i + 1][j - 1]
                            bl_box.reveal()

                        # try:
                        #     b_box = self.game_board[i + 1][j]
                        #     b_box.reveal()
                        # except IndexError:
                        #     b_box = False

                        # --- Bottom right
                        if j < self.cols - 1:
                            br_box = self.game_board[i + 1][j + 1]
                            br_box.reveal()
                        
                        # try:
                        #     br_box = self.game_board[i + 1][j + 1]
                        #     br_box
                        # except IndexError:
                        #     br_box = False
                    break

    def add_to_flaggeds(self):
        self.flagged_mines += 1

    def subtract_from_flaggeds(self):
        self.flagged_mines -= 1

    def get_box(self, row, col):
        return self.game_board[row][col]

    def act_to_box(self, box, act):
        if act == "r":
            if box.adjacent_mines == 0:
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
        self.coord = (self.row, self.col)
        self.mine = False
        self.revealed = False
        self.flag = False
        self.adjacent_mines = None

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
                return str(self.adjacent_mines)
                
                # Line for return a blank space (" ") instead of 0 when adjacent_mines is 0 ↴
                # return str(self.adjacent_mines if self.adjacent_mines > 0 else " ")
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