# Board values
DEFAULT_ROWS = 9
DEFAULT_COLS = 9
DEFAULT_MINES_RATIO = 15
DEFAULT_STYLE = "simple"

# Difficulty
DIFFICULTIES = {
    "begginer" : { # 9x9 board, 12 mines
        "rows": DEFAULT_ROWS,
        "cols": DEFAULT_COLS,
        "mines ratio": DEFAULT_MINES_RATIO,
    },
    "intermediate" : { # 16x16 board, 46 mines
        "rows": 16,
        "cols": 16,
        "mines ratio": 18,
    },
    "expert": { # 30x16 board, 101 mines
        "rows": 16,
        "cols": 30,
        "mines ratio": 21,
    }
}

DEFAULT_DIFFICULTY = DIFFICULTIES["begginer"]

# Box appearance
EMPTY = " "
MINE = "X"
FLAG = "F"
BOX = "■"