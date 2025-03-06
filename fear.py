import tkinter as tk

# Configuration
CELL_SIZE = 20      # pixel size of each grid square
GRID_COLS = 48      # number of columns (horizontal)
GRID_ROWS = 38      # number of rows (vertical)

LETTER_HEIGHT = 12
LETTER_WIDTH = 8
LETTER_GAP = 1      # gap between letters (in grid columns)

# Define block-letter F:
def create_F():
    pattern = []
    # Top horizontal bar.
    pattern.append([1]*LETTER_WIDTH)
    # Next three rows: only the left column is filled.
    for r in range(1, 4):
        pattern.append([1] + [0]*(LETTER_WIDTH - 1))
    # Middle horizontal bar.
    pattern.append([1]*LETTER_WIDTH)
    # Remaining rows: left column only.
    for r in range(5, LETTER_HEIGHT):
        pattern.append([1] + [0]*(LETTER_WIDTH - 1))
    return pattern

# Define block-letter E (vertical bar on left plus three horizontal bars):
def create_E():
    pattern = []
    for r in range(LETTER_HEIGHT):
        if r == 0 or r == LETTER_HEIGHT//2 or r == LETTER_HEIGHT - 1:
            pattern.append([1]*LETTER_WIDTH)
        else:
            pattern.append([1] + [0]*(LETTER_WIDTH - 1))
    return pattern

# Define block-letter A (manually designed):
def create_A():
    raw = [
        "00011000",
        "00100100",
        "01000010",
        "01000010",
        "01111110",
        "01000010",
        "01000010",
        "01000010",
        "01000010",
        "01000010",
        "01000010",
        "01000010",
    ]
    pattern = []
    for row in raw:
        pattern.append([int(ch) for ch in row])
    return pattern

# Define block-letter R (with a top bar, vertical left bar, and a diagonal leg):
def create_R():
    raw = [
        "11111111",
        "10000001",
        "10000001",
        "10000001",
        "11111111",
        "10100000",
        "10010000",
        "10001000",
        "10000100",
        "10000010",
        "10000001",
        "10000000",
    ]
    pattern = []
    for row in raw:
        pattern.append([int(ch) for ch in row])
    return pattern

# Create the letter patterns.
F_pattern = create_F()
E_pattern = create_E()
A_pattern = create_A()
R_pattern = create_R()

# Calculate the total width (in grid columns) that the word will occupy.
total_word_width = 4 * LETTER_WIDTH + 3 * LETTER_GAP  # 4 letters and 3 gaps

# Center the word horizontally (ensuring at least a 1-square margin on left/right).
horizontal_margin = (GRID_COLS - total_word_width) // 2
offsets = [horizontal_margin + i * (LETTER_WIDTH + LETTER_GAP) for i in range(4)]

# Center the letters vertically.
vertical_offset = (GRID_ROWS - LETTER_HEIGHT) // 2

# Create the main tkinter window and canvas.
root = tk.Tk()
root.title("FEAR on a 48x38 Grid")

canvas_width = GRID_COLS * CELL_SIZE
canvas_height = GRID_ROWS * CELL_SIZE
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Draw grid lines (optional, for visual clarity).
for i in range(GRID_COLS + 1):
    x = i * CELL_SIZE
    canvas.create_line(x, 0, x, canvas_height, fill="lightgray")
for j in range(GRID_ROWS + 1):
    y = j * CELL_SIZE
    canvas.create_line(0, y, canvas_width, y, fill="lightgray")

# Helper function to draw a letter pattern on the canvas.
def draw_pattern(pattern, top_left_x, top_left_y, color="red"):
    for r, row in enumerate(pattern):
        for c, cell in enumerate(row):
            if cell == 1:
                x0 = (top_left_x + c) * CELL_SIZE
                y0 = (top_left_y + r) * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

# Draw each letter in the word "FEAR".
for i, pat in enumerate([F_pattern, E_pattern, A_pattern, R_pattern]):
    draw_pattern(pat, offsets[i], vertical_offset)

# --- Add labels to the grid ---

# Bottom edge: label each column (1 to 48).
for col in range(GRID_COLS):
    x = col * CELL_SIZE + CELL_SIZE/2
    y = (GRID_ROWS - 1) * CELL_SIZE + CELL_SIZE/2
    canvas.create_text(x, y, text=str(col+1), font=("Arial", 8), fill="blue")

# Left edge: label the bottom 24 squares of the left column (numbered 1 to 24).
for row in range(GRID_ROWS - 24, GRID_ROWS):
    x = CELL_SIZE/2
    y = row * CELL_SIZE + CELL_SIZE/2
    label = row - (GRID_ROWS - 24) + 1
    canvas.create_text(x, y, text=str(label), font=("Arial", 8), fill="blue")

root.mainloop()
