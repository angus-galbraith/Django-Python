'''
This version will 501 as well. 
Menu items will be new game with drop down for each game, 
and High Scores with drop down for each game also for a player.
'''


import tkinter as tk
from tkinter import ttk
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
 

class FiveOhOne(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='501 Page', bg='pink')
        label.grid(column=0, row=0, sticky='news')

 
class RoundTheBoard(tk.Frame):
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
 
 
class Finishes(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Finish Page', bg='tomato')
        label.grid(column=0, row=0, sticky='news')
 
 
class HighScores(tk.Frame):
    '''
        HighScores class displays all scores
    '''
    def __init__(self,):
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
        '''for name, score in data:
            label = tk.Label(container, text=f'{name.title()}: {score}', bg='lightgray', anchor='w', padx=8)
            label['font'] = (None, 14, 'normal')
            label['highlightbackground'] = 'black'
            label['highlightcolor'] = 'black'
            label['highlightthickness'] = 1
            label.grid(column=0, row=row, sticky='new', ipadx=5, padx=3)
            row += 1
        ''' 
 
 
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
        self.page1 = Main()
        self.page1.grid(column=0, row=0, sticky='news')
        self.page1.grid_columnconfigure(0, weight=3)
        self.page1.grid_rowconfigure(0, weight=3)


        self.page2 = FiveOhOne()
        self.page2.grid(column=0, row=0, sticky='news')
        self.page2.grid_columnconfigure(0, weight=3)
        self.page2.grid_rowconfigure(0, weight=3)
 
        page3 = RoundTheBoard()
        page3.grid(column=0, row=0, sticky='news')
        page3.grid_columnconfigure(0, weight=3)
        page3.grid_rowconfigure(0, weight=3)
 
        page4 = Finishes()
        page4.grid(column=0, row=0, sticky='news')
        page4.grid_columnconfigure(0, weight=3)
        page4.grid_rowconfigure(0, weight=3)
 
        page5 = HighScores()
        page5.grid(column=0, row=0, sticky='news')
        page5.grid_columnconfigure(0, weight=3)
        page5.grid_rowconfigure(0, weight=3)
 
        
 
        # Setup the menus and commands
        game_menu = tk.Menu(self.window.menubar, tearoff=0)
        game_menu.add_command(label='501', command=lambda: self.newGame(self.page2))
        game_menu.add_command(label='Round the Board', command=page3.tkraise)
        game_menu.add_command(label='Finishes', command=page5.tkraise)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        score_menu = tk.Menu(self.window.menubar, tearoff=0)
        score_menu.add_command(label='501 Averages', command=lambda: self.newGame(self.page1))
        score_menu.add_command(label='Round the Board', command=page3.tkraise)
        score_menu.add_command(label='Finishes', command=page3.tkraise)
        score_menu.add_command(label='High Scores', command=page4.tkraise)
 
        #page_menu.add_separator()
        #page_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        self.window.menubar.add_cascade(label='New Game', menu=game_menu)
        self.window.menubar.add_cascade(label='High Scores', menu=score_menu)

    def newGame(self, page):
        page = page
        if page == self.page1:
            self.page1.tkraise()
        elif page == self.page2:
            self.page2.tkraise()
 
    
 
 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400+300+300')
    controller = Controller(Database(), Window(root))
    root.mainloop()