'''
This version will 501 as well. 
Menu items will be new game with drop down for each game, 
and High Scores with drop down for each game also for a player.
'''


import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
 
import tkinter as tk
import sqlite3 as sq
 
class Database:
    '''
        Database class handles all the database functions.
        Create, insert, and retrieve
    '''
    def __init__(self):
        self.tables = ('rtbhigh', 'finisheshigh')
        self.connection = sq.connect('highscores.db')
        self.cursor = self.connection.cursor()
 
    def create_tables(self):
        self.cursor.execute('''
            create table if not exists rtbhigh (
            playername text, score integer
            )
        ''')
 
        self.cursor.execute('''
            create table if not exists finisheshigh (
            playername text, score integer
            )
        ''')
        self.connection.commit()
 
 
    def insert(self, playername, score, table):
        self.cursor.execute(f'insert into {table} (playername, score) values(?,?)', (playername, score))
        self.connection.commit()
             
    def getall(self, table):
        query = self.cursor.execute(f'select * from {table} order by score desc').fetchall()
        print(query)
        return query
 
 
class Rtb(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Rtb Page', bg='pink')
        label.grid(column=0, row=0, sticky='news')
 
 
class Main(tk.Frame):
    ''' Main class is the start/landing page '''
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Main Page', bg='gold')
        label.grid(column=0, row=0, sticky='news')
 
 
class Finish(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Finish Page', bg='tomato')
        label.grid(column=0, row=0, sticky='news')
 
 
class HighScore(tk.Frame):
    '''
        HighScores class displays all scores
    '''
    def __init__(self, data):
        tk.Frame.__init__(self)
        container = tk.Frame(self)
        container.grid(column=0, row=0, sticky='new')
        container.grid_columnconfigure(0, weight=3)
 
        header = tk.Label(container, text='High Scores', bg='gray')
        header['font'] = (None, 18, 'bold')
        header['highlightbackground'] = 'black'
        header['highlightcolor'] = 'black'
        header['highlightthickness'] = 1
        header.grid(column=0, row=0, sticky='new', padx=3, pady=(0, 8))
 
        row = 1
        for name, score in data:
            label = tk.Label(container, text=f'{name.title()}: {score}', bg='lightgray', anchor='w', padx=8)
            label['font'] = (None, 14, 'normal')
            label['highlightbackground'] = 'black'
            label['highlightcolor'] = 'black'
            label['highlightthickness'] = 1
            label.grid(column=0, row=row, sticky='new', ipadx=5, padx=3)
            row += 1
 
 
class NewGame(tk.Frame):
    ''' NewGame class page for starting new games '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = tk.Label(self, text='Start a new game', bg='burlywood')
        label['font'] = (None, 16, 'normal')
        label.grid(column=0, row=0, sticky='new')
 
 
class Window(tk.Frame):
    ''' Window class is for the menus and container'''
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        parent.title('Test Application')
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
 
        self.menubar = tk.Menu(parent)
        parent.configure(menu=self.menubar)
 
 
 
class Controller:
    ''' Controller class ties all the classes together '''
    def __init__(self, database, window):
        self.db = database
        self.window = window
        self.db.create_tables()
        # self.db.insert('john doe', 15, self.db.tables[1])
        # self.db.insert('jane doe', 25, self.db.tables[1])
        # self.db.insert('child doe', 5, self.db.tables[1])
         
 
        # Setup the pages by calling the appropiate class
        page2 = Rtb()
        page2.grid(column=0, row=0, sticky='news')
        page2.grid_columnconfigure(0, weight=3)
        page2.grid_rowconfigure(0, weight=3)
 
        page3 = Finish()
        page3.grid(column=0, row=0, sticky='news')
        page3.grid_columnconfigure(0, weight=3)
        page3.grid_rowconfigure(0, weight=3)
 
        page4 = HighScore(self.get_scores())
        page4.grid(column=0, row=0, sticky='news')
        page4.grid_columnconfigure(0, weight=3)
        page4.grid_rowconfigure(0, weight=3)
 
        page5 = NewGame()
        page5.grid(column=0, row=0, sticky='news')
        page5.grid_columnconfigure(0, weight=3)
        page5.grid_rowconfigure(0, weight=3)
 
        page1 = Main()
        page1.grid(column=0, row=0, sticky='news')
        page1.grid_columnconfigure(0, weight=3)
        page1.grid_rowconfigure(0, weight=3)
 
        # Setup the menus and commands
        game_menu = tk.Menu(self.window.menubar, tearoff=0)
        game_menu.add_command(label='New Game', command=page5.tkraise)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        page_menu = tk.Menu(self.window.menubar, tearoff=0)
        page_menu.add_command(label='Main Page', command=page1.tkraise)
        page_menu.add_command(label='RTB Page', command=page2.tkraise)
        page_menu.add_command(label='Finish Page', command=page3.tkraise)
        page_menu.add_command(label='High Scores', command=page4.tkraise)
 
        page_menu.add_separator()
        page_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        self.window.menubar.add_cascade(label='Game Options', menu=game_menu)
        self.window.menubar.add_cascade(label='Pages', menu=page_menu)
 
    def get_scores(self):
        ''' Method for getting scores '''
        data = self.db.getall(self.db.tables[1])
        print(data)
        return data
 
 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400+300+300')
    controller = Controller(Database(), Window(root))
    root.mainloop()