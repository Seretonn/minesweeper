import tkinter as tk
from tkinter import ttk
import game

class App(tk.Tk):
    def __init__(self, title, size):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}+50+50")
        self.minsize(size[0], size[1])

        # game
        self.game = game.Game()

        # widgets
        self.top_section = Top_section(self)
        self.board = Board(self)

        # run
        self.mainloop()

class Top_section(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.2)

        self.create_widgets()

    def create_widgets(self):
        flagged_boxes_label = ttk.Label(self, text="Flagged\nboxes")
        new_game_button = ttk.Button(self, text="New game")
        timer_label = ttk.Label(self, text="timer")

        flagged_boxes_label.pack(side="left", padx=10)
        new_game_button.pack(side="left", expand=True, fill="y", padx=10)
        timer_label.pack(side="right", padx=10)

class Board(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=1)
        self.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
        self.rowconfigure()

        # ttk.Label(self, text="Board", background="blue").pack(expand=True, fill="both")

    def create_grid(self):
        # for row in range
        pass

if __name__ == "__main__":
    App("Minesweeper", (400, 400))