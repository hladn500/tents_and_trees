from tkinter import *
from classes import Cell, LineInfo
from solution import solve
import settings


root = Tk()

root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Tents and Trees Solver")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=100,
)
top_frame.place(x=0, y=0)

top_strip = Frame(
    root,
    bg='black',
    width=1080,
    height=80,
)
top_strip.place(x=360, y=100)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Tents and Trees Solver',
    font=('', 48),
)
game_title.place(x=360, y=0)

left_frame = Frame(
    root,
    bg='black',
    width=270,
    height=540,
)
left_frame.place(x=0, y=180)

left_strip = Frame(
    root,
    width=80,
    height=540,
)
left_strip.place(x=270, y=180)

center_frame = Frame(
    root,
    bg='black',
    width=1080,
    height=540,
)
center_frame.place(x=360, y=180)

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x, row=y)

for x in range(settings.GRID_SIZE):
    col = LineInfo('column', x)
    col.create_btn_object(top_strip)
    col.line_btn_object.grid(row=0, column=x)

for y in range(settings.GRID_SIZE):
    row = LineInfo('row', y)
    row.create_btn_object(left_strip)
    row.line_btn_object.grid(row=y, column=0)

solve_btn = Button(
    left_frame,
    bg='red',
    text='SOLVE',
    width=10,
    height=2,
)
solve_btn.place(x=150, y=0)
solve_btn.bind('<Button-1>', solve)

root.mainloop()
