import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import game as ms

class App(tk.Tk):
    def __init__(self, title, size):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}+50+50")
        self.minsize(size[0], size[1])
        self.maxsize(size[0], size[1])

        # game
        self.game = None # ms.Game()
        self.board = ms.Board()

        # widgets
        self.top_section = Top_section(self)
        self.board_section = Board_section(self, self.board)

        # run
        self.mainloop()

class Top_section(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.1)

        self.images = {}

        self.load_images()
        self.create_widgets()

    def load_images(self):
        self.images["smiley_doggy"] = ImageTk.PhotoImage(Image.open("lovethismfdog.png").resize((35, 30))) #tk.PhotoImage(file=)
        self.images["sad_doggy"] = None

    def create_widgets(self):
        flagged_boxes_label = ttk.Label(self, text="Flagged\nboxes")
        new_game_button = ttk.Button(self, text="New game", image=self.images.get("smiley_doggy"), command = lambda: print("New game"))
        timer_label = ttk.Label(self, text="Timer")

        flagged_boxes_label.pack(side="left", padx=10)
        new_game_button.pack(side="left", expand=True, fill="y", padx=10)
        timer_label.pack(side="right", padx=10)

class Board_section(ttk.Frame):
    def __init__(self, parent, board_obj):
        super().__init__(parent, padding=1)

        # setup
        self.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        self.board = board_obj
        self.create_board(self.board)

    def create_board(self, board):
        for i, row in enumerate(board.game_board):
            self.columnconfigure(i, weight=1, uniform="a")
            for j, box in enumerate(row):
                if i == 0: 
                    self.rowconfigure(j, weight=1, uniform="a")
                button = ttk.Button(self)
                button.grid(row=i, column=j, sticky="nsew")
                button.bind("<Button-1>", lambda event, row=i, col=j: self.left_click(row, col))
                button.bind("<Button-3>", lambda event, row=i, col=j: self.right_click(row, col))
            pass
        pass

    def left_click(self, row, col):
        print(f"Left click! (reveal) {row}, {col}")

    def right_click(self, row, col):
        print(f"Right click! (put/remove flag) {row}, {col}")

if __name__ == "__main__":
    App("Minesweeper", (400, 400))