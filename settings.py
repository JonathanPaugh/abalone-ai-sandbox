from tkinter import Tk, OptionMenu, StringVar, Entry
from tkinter.ttk import Frame, Label, Button

root = Tk()
root.title("Abalone Settings")

frame = Frame(root, padding=10)
frame.grid()

Label(frame, text="Settings", font="Helvetica 16 bold").grid(column=0, row=0, columnspan=2)

Label(frame, text="Starting Layout").grid(column=0, row=1, sticky='e', ipadx=8)
starting_layout = StringVar(frame)
starting_layout.set("Standard")
OptionMenu(frame, starting_layout, "Standard", "German Daisy", "Belgian Daisy").grid(column=1, row=1, sticky='w')


Label(frame, text="Game Mode").grid(column=0, row=2, sticky='e', ipadx=8)
game_mode = StringVar(frame)
game_mode.set("Human vs. Computer")
OptionMenu(frame, game_mode, "Human vs. Computer", "Computer vs. Computer", "Human vs. Human").grid(column=1, row=2, sticky='w')


Label(frame, text="Player Color").grid(column=0, row=3, sticky='e', ipadx=8)
player_color = StringVar(frame)
player_color.set("White")
OptionMenu(frame, player_color, "White", "Black").grid(column=1, row=3, sticky='w')


Label(frame, text="Move Limit").grid(column=0, row=4, sticky='e', ipadx=8)
frame_move_limit = Frame(frame)
frame_move_limit.grid(column=1, row=4, sticky='w')

entry_move_limit_p1 = Entry(frame_move_limit, width=5)
entry_move_limit_p1.insert(0, "50")
entry_move_limit_p1.grid(column=0, row=0, sticky='w')

entry_move_limit_p2 = Entry(frame_move_limit, width=5)
entry_move_limit_p2.insert(0, "50")
entry_move_limit_p2.grid(column=1, row=0, sticky='w', padx=8)


Label(frame, text="Time Limit").grid(column=0, row=5, sticky='e', ipadx=8)
frame_time_limit = Frame(frame)
frame_time_limit.grid(column=1, row=5, sticky='w')

entry_time_limit_p1 = Entry(frame_time_limit, width=5)
entry_time_limit_p1.insert(0, "5s")
entry_time_limit_p1.grid(column=0, row=0, sticky='w')

entry_time_limit_p2 = Entry(frame_time_limit, width=5)
entry_time_limit_p2.insert(0, "5s")
entry_time_limit_p2.grid(column=1, row=0, sticky='w', padx=8)


Button(frame, text="Confirm", command=root.destroy).grid(column=0, row=6, columnspan=2)

col_count, row_count = frame.grid_size()

for col in range(col_count):
    frame.grid_columnconfigure(col, minsize=200)

for row in range(row_count):
    frame.grid_rowconfigure(row, minsize=40)

root.mainloop()
