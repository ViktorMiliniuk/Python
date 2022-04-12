import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False
        self.number = number
        self.bombs = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number}'


class MineSweeper():
    ROW = 10
    COLUMNS = 7
    window = tk.Tk()
    MINES = 7
    GAME_OVER = False
    FIRST_CLICK = True
    ALL_CLICKED = 2
    NEED_TO_BE_CLICKED = ROW * COLUMNS - MINES
    GAME_WIN = False

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW + 2):
            tmp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                tmp.append(btn)
            self.buttons.append(tmp)

    def right_click(self, event):
        if MineSweeper.GAME_OVER:
            return False
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):
        self.only_mines_left()
        print(self.ALL_CLICKED, self.NEED_TO_BE_CLICKED)
        if MineSweeper.GAME_OVER:
            return False
        if MineSweeper.FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            MineSweeper.FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red')
            MineSweeper.GAME_OVER = True
            showinfo('Game over', 'You lose')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'

        else:
            self.search(clicked_button)
        clicked_button.config(state='disabled', disabledforeground='black')
        clicked_button.config(relief=tk.SUNKEN)
        clicked_button.is_open = True
        MineSweeper.ALL_CLICKED += 1
        self.only_mines_left()

    def only_mines_left(self):
        if MineSweeper.ALL_CLICKED == MineSweeper.NEED_TO_BE_CLICKED:
            MineSweeper.GAME_WIN = True
            showinfo('Congratulations!', 'YOU WIN!')

    def search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur = queue.pop()
            self.ALL_CLICKED += 1
            if cur.bombs:
                cur.config(text=cur.bombs)
            else:
                cur.config(text='')
            cur.config(state='disabled', disabledforeground='black')
            cur.config(relief=tk.SUNKEN)
            cur.is_open = True

            self.only_mines_left()

            if cur.bombs == 0:
                x, y = cur.x, cur.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and 1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.FIRST_CLICK = True
        MineSweeper.GAME_OVER = False
        self.ALL_CLICKED = 1

    def create_settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Settings')
        tk.Label(win_settings, text='Rows number').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Columns number').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Mines number').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='OK',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Error', 'Wrong value')
            return False
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        MineSweeper.ALL_CLICKED = 0
        NEED_TO_BE_CLICKED = row.get() * column.get() - mines.get()
        self.reload()

    def create_widgets(self):

        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label='New game', command=self.reload)
        settings_menu.add_command(label='Settings', command=self.create_settings_window)
        settings_menu.add_command(label='Exit', command=self.window.destroy)
        menu.add_cascade(label='Menu', menu=settings_menu)

        counter = 1
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = counter
                btn.grid(row=i, column=j, stick='NWES')
                counter += 1

        for i in range(1, MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for j in range(1, MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red')
                else:
                    if btn.bombs == 0:
                        btn.config(text='')
                    else:
                        btn.config(text=btn.bombs)

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.bombs, end='')
            print()

    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                bombs = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                bombs += 1
                btn.bombs = bombs

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[: MineSweeper.MINES]

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True


if __name__ == __main__:
    game = MineSweeper()
    game.start()
