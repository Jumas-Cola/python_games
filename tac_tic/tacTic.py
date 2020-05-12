import random
import copy
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from functools import partial


class Game:

    def __init__(self, player_sign, difficulty=0.8, field_size=3):
        self.player_sign = player_sign
        self.difficulty = difficulty * 3
        self.computer_sign = 'X' if player_sign == 'O' else 'O'
        self.next_step = 'X'
        self.game_field = [['' for _ in range(field_size)]
                               for _ in range(field_size)]
        if self.next_step == self.computer_sign:
            self.computer_step()


    def upd_next_step(self):
        self.next_step = 'X' if self.next_step == 'O' else 'O'


    def empty_cells(self, field=None):

        if field is not None:
            game_field = field
        else:
            game_field = self.game_field

        return [(i, j) for i, row in enumerate(game_field)
                       for j in range(len(row))
                       if row[j] != self.player_sign
                       and row[j] != self.computer_sign]

    def print_game_field(self):

        for row in self.game_field:
            print('|{:_>1}{:_>1}{:_>1}|'.format(*row))
        print()


    def player_step(self, cell=None):

        self.upd_next_step()

        if cell is not None:
            cell = tuple(int(i) for i in cell.strip().split())
            self.game_field[cell[0]][cell[1]] = self.player_sign
        else:
            cell = input('Please, write cell addres:\n')
            cell = tuple(int(i) for i in cell.split())
            while cell not in self.empty_cells():
                cell = input('\nIncorrect cell, choose another:\n')
                cell = tuple(int(i) for i in cell.strip().split())
            self.game_field[cell[0]][cell[1]] = self.player_sign


    def computer_step(self):

        self.upd_next_step()

        emptys = self.empty_cells()

        if len(self.game_field)**2 - len(emptys) <= 3 - self.difficulty:
            x, y = random.choice(emptys)
        else:
            step = self.best_step('computer')
            if 'index' in step:
                x, y = step['index']
            else:
                return

        self.game_field[x][y] = self.computer_sign


    def check_win(self, actor, field=None):

        if field is not None:
            game_field = field
        else:
            game_field = self.game_field

        if actor == 'player':
            sign = self.player_sign
        else:
            sign = self.computer_sign

        if all(item == sign for i, row in enumerate(game_field)
                            for j, item in enumerate(row) if i == j):
            return True

        if all(item == sign for i, row in enumerate(game_field)
                            for j, item in enumerate(row) if i == len(row) - j - 1):
            return True

        for row in game_field:
            if all(i == sign for i in row):
                return True

        for col in range(len(game_field[0])):
            if all(row[col] == sign for row in game_field):
                return True

        return False


    def best_step(self, actor, field=None):

        if field is not None:
            game_field = copy.deepcopy(field)
        else:
            game_field = copy.deepcopy(self.game_field)

        if actor == 'player':
            sign = self.player_sign
        else:
            sign = self.computer_sign

        array = self.empty_cells(game_field)

        if self.check_win('player', game_field):
            return {'score': -10}
        elif self.check_win('computer', game_field):
            return {'score': 10}
        elif not len(array):
            return {'score': 0}

        moves = []
        for i in array:
            move = {}
            x, y = i
            move['index'] = game_field[x][y]
            game_field[x][y] = sign

            if sign == self.computer_sign:
                g = self.best_step('player', game_field)
            else:
                g = self.best_step('computer', game_field)
            move['score'] = g['score']

            game_field[x][y] = move['index']
            move['index'] = i
            moves.append(move)

        best_move = None

        if sign == self.computer_sign:
            best_score = float('-inf')
            for i in moves:
                if i['score'] > best_score:
                    best_score = i['score']
                    best_move = i
        else:
            best_score = float('inf')
            for i in moves:
                if i['score'] < best_score:
                    best_score = i['score']
                    best_move = i

        return best_move


    def check_draw(self):
        if not self.empty_cells() and \
           not self.check_win('player') and \
           not self.check_win('computer'):
               return True
        return False


class TacTic(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.colorscheme = {
                'bg_color': '#3914AF',
                'btns_color': '#C8B7FF'
                }

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry('300x300')
        try:
            self.cross_img = PhotoImage(file='cross.png')
        except:
            pass
        try:
            self.zero_img = PhotoImage(file='zero.png')
        except:
            pass
        self.pixel = PhotoImage(width=1, height=1)

        self.frames = {}
        for F in (ChooseSign, GameField):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('ChooseSign')


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


    def get_page(self, page_class):
        return self.frames[page_class]


class ChooseSign(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.colorscheme['bg_color'])
        self.controller = controller

        try:
            bg = controller.colorscheme['btns_color']
            img = controller.cross_img
        except:
            bg = '#000'
            img = controller.pixel

        X = tk.Button(self, height=70, width=70,
                image=img,
                background=bg,
                activebackground=bg,
                border=0,
                command=partial(self.click_handler, 'X')
                )
        try:
            bg = controller.colorscheme['btns_color']
            img = controller.zero_img
        except:
            bg = '#fff'
            img = controller.pixel

        O = tk.Button(self, height=70, width=70,
                image=img,
                background=bg,
                activebackground=bg,
                border=0,
                command=partial(self.click_handler, 'O')
                )

        X.grid(row=1, column=1)
        O.grid(row=1, column=3)

        self.difficulty = tk.Scale(self, from_=1, to=3,
                resolution=1,
                orient=tk.HORIZONTAL,
                background=controller.colorscheme['btns_color'],
                )
        self.difficulty.set(2)
        self.difficulty.grid(row=3, column=1, columnspan=3, sticky='nesw')

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)


    def click_handler(self, sign):
        page = self.controller.get_page('GameField')
        page.game = Game(sign, difficulty=self.difficulty.get() / 3)
        page.refresh_field()
        self.controller.show_frame('GameField')


class GameField(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.colorscheme['bg_color'])
        self.controller = controller
        self.game = Game('X')

        self.buttons = []
        self.refresh_field()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)


    def refresh_field(self):
        if self.buttons:
            for row in self.buttons:
                for button in row:
                    button.destroy()
        self.buttons = []
        for i, row in enumerate(self.game.game_field):
            btn_row = []
            for j, item in enumerate(row):
                if item == 'X':
                    try:
                        img = self.controller.cross_img
                        bg = self.controller.colorscheme['btns_color']
                    except:
                        bg = '#000'
                        img = self.controller.pixel
                elif item == 'O':
                    try:
                        img = self.controller.zero_img
                        bg = self.controller.colorscheme['btns_color']
                    except:
                        bg = '#fff'
                        img = self.controller.pixel
                else:
                    img = self.controller.pixel
                    bg = self.controller.colorscheme['btns_color']

                button = tk.Button(self, height=70, width=70,
                        image=img,
                        background=bg,
                        activebackground=bg,
                        border=0,
                        command=partial(self.click_handler, (i, j))
                        )
                button.grid(row=i + 1, column=j + 1, padx=3, pady=3)
                btn_row.append(button)
            self.buttons.append(btn_row)


    def click_handler(self, coords):
        i, j = coords
        if coords in self.game.empty_cells() and \
        self.game.next_step == self.game.player_sign:
            self.game.player_step('{} {}'.format(i, j))
            self.refresh_field()
            if self.game.check_win('player'):
                messagebox.showinfo('Info', 'You Win!')
                self.after(500, self.show_choose_frame)
                return
            if self.game.check_draw():
                messagebox.showinfo('Info', 'Draw!')
                self.after(500, self.show_choose_frame)
                return
            self.after(10, self.computer_step)


    def computer_step(self):
        self.game.computer_step()
        self.refresh_field()
        if self.game.check_win('computer'):
            messagebox.showinfo('Info', 'Computer Win!')
            self.after(500, self.show_choose_frame)
            return
        if self.game.check_draw():
            messagebox.showinfo('Info', 'Draw!')
            self.after(500, self.show_choose_frame)
            return


    def show_choose_frame(self):
        self.controller.show_frame('ChooseSign')



if __name__ == '__main__':
    app = TacTic()
    app.mainloop()
