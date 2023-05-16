import os

W = 1024  # screen width
H = 600  # screen height

CELL_SIZE = 20
COL_COUNT = W // CELL_SIZE  # column number - width in cells
ROW_COUNT = H // CELL_SIZE  # column number - height in cells

image = os.path.join("images", "part.png")  # snake tile

# fonts
LARGE_FONT = ("Tahoma", 55)
NORM_FONT = ("Verdana", 10)
SCORE_FONT = ("Tahoma", 30)

# RGB colors
RED = (255, 50, 30)
BLUE = (50, 80, 255)
BLACK = (0, 0, 0)
TURQUOISE = (0, 230, 230)
