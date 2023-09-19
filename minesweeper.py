from tkinter import *
from tkinter import ttk
from numpy import *
import random


root = Tk()
root.title('Minesweeper')
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, E, W, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
difficulty = StringVar(mainframe)
difficulty.set('Easy')
diff_tuple = (10, 10)

OPTIONS = [
    'Easy',
    'Medium',
    'Hard',
    'Extreme'
]

w = OptionMenu(mainframe, difficulty, *OPTIONS)
w.pack()


def gen():
    global difficulty, diff_tuple
    difficulty_dict = {
        0: (10, 10),
        1: (12, 20),
        2: (14, 40),
        3: (8, 35)
    }
    diff_tuple = difficulty_dict[OPTIONS.index(difficulty.get())]
    generate()


gen_button = Button(mainframe, command=gen, text='Generate')
gen_button.pack()


def generate():
    global diff_tuple
    side, mines = diff_tuple[0], diff_tuple[1]
    randomlist = random.sample(range(1, side**2 - 1), mines)
    coordinates = [(x%side-1, x//side-1) for x in randomlist]
    field = zeros((side,side))
    for c in coordinates:
        field[c[0]][c[1]] = 1
    _f = pad(field, 1 ,mode='constant')
    minefield = zeros_like(_f)
    for x in range(1, side+1):
        for y in range(1, side+1):
            if _f[x][y] == 1:
                minefield[x][y] = 9
            else:
                minefield[x][y] = sum(_f[x - 1:x + 2, y - 1:y + 2].flatten())
    minefield = minefield[1:side+1,1:side+1]
    sweeper(minefield, side)


def sweeper(minefield, side):
    global root, difficulty
    root.destroy()
    root_2 = Tk()
    root_2.title(f'Minesweeper:{difficulty}')
    main_field = Canvas(root_2, width=side*20, height=side*20, background='white')
    for x in range(0, side*20, 20):
        main_field.create_line(x, 0, x, side*20, fill='black')
    for y in range(0, side*20, 20):
        main_field.create_line(0, y, side*20, y, fill='black')
    main_field.pack()

    def win():
        if 9 not in minefield and 109 not in minefield:
            main_field.create_rectangle(0, 0, side * 20, side * 20, fill='gray')
            main_field.create_text(side * 10, side * 10, text=f'You won!!!', fill='white', font='Helvetica 15')

    def loose():
        main_field.create_rectangle(0, 0, side * 20, side * 20, fill='gray')
        main_field.create_text(side * 10, side * 10, text=f'Try Again :c', fill='white', font='Helvetica 15')
        for x in range(side):
            for y in range(side):
                minefield[x][y] += 100

    def reveal(event):
        global xpos, ypos
        xpos, ypos = event.x, event.y
        x, y = int(xpos // 20), int(ypos // 20)

        tile = minefield[x][y]
        if 0 < tile < 9:
            main_field.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill='gray')
            main_field.create_text(x * 20 + 10, y * 20 + 10, text=f'{int(tile)}', fill='white', font='Helvetica 15')
        elif tile == 9:
            main_field.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill='gray')
            main_field.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill='red')
            loose()
        elif tile == 0:
            map = area_reveal(x, y)
            for (x, y) in map:
                tile = minefield[x][y]
                if 0 < tile < 9:
                    main_field.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill='gray')
                    main_field.create_text(x * 20 + 10, y * 20 + 10, text=f'{int(tile)}', fill='white',
                                           font='Helvetica 15')
                else:
                    main_field.create_rectangle(x*20, y*20, x*20 + 20, y*20 + 20, fill='gray')

    def flag(event):
        global xpos, ypos
        xpos, ypos = event.x, event.y
        x, y = int(xpos // 20), int(ypos // 20)
        tile = minefield[x][y]
        if tile < 10:
            main_field.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill='blue')
            minefield[x][y] += 10
        elif 10 <= tile < 100:
            main_field.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill='white')
            minefield[x][y] += -10

    def area_reveal(x, y):
        vis = []
        shifts = [
            (-1, -1),
            (-1, 1),
            (-1, 0),
            (1, -1),
            (1, 1),
            (1, 0),
            (0, -1),
            (0, 1),
        ]
        # main loop
        to_reveal = []
        if (x, y) not in vis:
            to_reveal.append((x, y))

        while to_reveal != []:
            cell = to_reveal.pop()
            vis.append(cell)
            if minefield[cell[0]][cell[1]] == 0:
                for shift in shifts:
                    if (cell[0] + shift[0], cell[1] + shift[1]) not in vis and 0 <= (cell[0] + shift[0]) <= 9 and 0 <= (
                            cell[1] + shift[1]) <= 9:
                        to_reveal.append((cell[0] + shift[0], cell[1] + shift[1]))
        return vis


    main_field.bind("<Button-1>", reveal)
    main_field.bind("<Button-3>", flag)
    win_cond = Button(root_2, text='Check for win', command=win)
    win_cond.pack()

    root_2.mainloop()


root.mainloop()