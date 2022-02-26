import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import scrolledtext

BOARD_SIZE = 5
MARBLE_XMARGIN = 4
MARBLE_YMARGIN = 1
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
MARBLE_SIZE = WINDOW_WIDTH / 10
BOARD_MAXCOLS = BOARD_SIZE * 2 - 1
BOARD_WIDTH = (MARBLE_SIZE + MARBLE_XMARGIN) * BOARD_MAXCOLS - MARBLE_XMARGIN
BOARD_HEIGHT = (MARBLE_SIZE + MARBLE_YMARGIN) * BOARD_MAXCOLS - MARBLE_YMARGIN
root = tk.Tk()


def generate_empty_board(size):
    board = []
    for i in reversed(range(size)):
        board.insert(0, [0] * (size + i))
        if i < size - 1:
            board.append([0] * (size + i))
    return board


def generate_standard_board():
    return [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 0, 0],
        [2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
    ]


def render_board(container, board, pos):
    canvas = Canvas(container, width=480, height=480, highlightbackground="black", highlightthickness=1,
                    background="#42464c")
    for row, line in enumerate(board):
        for col, val in enumerate(line):
            x = (col * (MARBLE_SIZE + MARBLE_XMARGIN)
                 + (BOARD_MAXCOLS - len(line)) * (MARBLE_SIZE + MARBLE_XMARGIN) / 2
                 + pos[0])
            y = (row * (MARBLE_SIZE + MARBLE_YMARGIN)
                 + pos[1])
            cell_data = board[row][col]
            circle_color = {
                0: "#ccc",
                1: "#c36",
                2: "#36c",
            }[cell_data]
            canvas.create_oval(x, y, x + MARBLE_SIZE, y + MARBLE_SIZE, fill=circle_color, outline="black", width=2)
    return canvas


def create_button_frame(container):
    frame = tk.Frame(container,  borderwidth=1, relief="solid", width=1000, background="#42464c")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, minsize=320)
    frame.columnconfigure(5, weight=1)

    ttk.Label(frame, text='00:00\':00\"', borderwidth=1, relief="solid", font=("Arial", 25)).grid(column=0, row=0)
    ttk.Button(frame, text='Pause').grid(column=1, row=0)
    ttk.Button(frame, text='Reset').grid(column=2, row=0)
    ttk.Button(frame, text='Undo').grid(column=3, row=0)
    ttk.Button(frame, text='Settings').grid(column=5, row=0)

    for widget in frame.winfo_children():
        widget.grid(padx=3, pady=0)

    return frame


def create_history_frame(container):
    frame = tk.Frame(container, background="#42464c",  borderwidth=1, relief="solid")

    ttk.Label(frame, background="#42464c", foreground="white",
              text="Move History", font=("Arial", 15), ).grid(column=0, row=0)

    # scrolled text
    text_area = scrolledtext.ScrolledText(frame,
                                          background="#42464c",
                                          foreground='white',
                                          wrap=tk.WORD,
                                          width=20,
                                          height=10,
                                          font=("Times New Roman",
                                                15))

    text_area.grid(column=0, pady=10, padx=10)

    return frame


def create_score_frame(container):
    frame = tk.Frame(container, background="#42464c", borderwidth=1, relief="solid")
    frame.columnconfigure(0, minsize=72)  # creates empty space
    frame.columnconfigure(1, weight=8)
    frame.columnconfigure(2, weight=8)
    frame.columnconfigure(3, minsize=72)  # creates empty space
    frame.rowconfigure(0, weight=8)
    frame.rowconfigure(1, weight=8)
    frame.rowconfigure(2, weight=8)
    frame.rowconfigure(3, minsize=5)  # creates empty space
    frame.rowconfigure(4, weight=8)
    frame.rowconfigure(5, weight=8)
    frame.rowconfigure(6, weight=8)

    tk.Label(frame, background="#42464c", foreground="white", text='Player1', font=("Arial", 15)).grid(column=1, row=0,
                                                                                                       columnspan=2)
    tk.Label(frame, background="#42464c", foreground="white", text='Score:', font=("Arial", 12)).grid(column=1, row=1)
    tk.Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=1)
    tk.Label(frame, background="#42464c", foreground="white", text='Moves:', font=("Arial", 12)).grid(column=1, row=2)
    tk.Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=2)
    tk.Label(frame, background="#42464c", foreground="white", text='Player2', font=("Arial", 15)).grid(column=1, row=4,
                                                                                                       columnspan=2)
    tk.Label(frame, background="#42464c", foreground="white", text='Score:', font=("Arial", 12)).grid(column=1, row=5)
    tk.Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=5)
    tk.Label(frame, background="#42464c", foreground="white", text='Moves:', font=("Arial", 12)).grid(column=1, row=6)
    tk.Label(frame, background="#42464c", foreground="white", text='Test', font=("Arial", 12)).grid(column=2, row=6)

    for widget in frame.winfo_children():
        widget.grid(padx=2, pady=5)
    return frame


def create_main_window():
    # root window
    root.title('Replace')
    root.geometry('800x600')
    # windows only (remove the minimize/maximize button)
    root.attributes('-toolwindow', True)
    root.configure(background="#36393E")
    # root.attributes('-fullscreen', True) #for fullscreen

    # layout on the root window
    root.columnconfigure(0, weight=8)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0, weight=2)
    root.rowconfigure(1, weight=4)
    root.rowconfigure(2, weight=4)

    button_frame = create_button_frame(root)
    button_frame.grid(column=0, row=0, columnspan=2)

    button_frame = create_score_frame(root)
    button_frame.grid(column=1, row=1)

    button_frame = create_history_frame(root)
    button_frame.grid(column=1, row=2)

    board_frame = render_board(root, generate_standard_board(), pos=(
        WINDOW_WIDTH / 2 - BOARD_WIDTH / 2,
        WINDOW_HEIGHT / 2 - BOARD_HEIGHT / 2
    ))
    board_frame.grid(column=0, row=1, rowspan=2)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
