import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
from tkinter import messagebox
 
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
        self.isActive = False
        self.gameActive = False
        tk.Frame.__init__(self)
        #label = tk.Label(self, text='Rtb Page', bg='pink')
        #label.grid(column=0, row=0, sticky='news')

        self.playerName = tk.StringVar()
        self.toGoFor = 1
        self.runningTotal = 0
        self.goFor = tk.IntVar()
        self.goFor.set(self.toGoFor)
        self.running = tk.IntVar()
        self.running.set(self.runningTotal)



    def start(self):
        self.startWindow = tk.Toplevel()
        self.startWindow.title("New Game")
        tk.Label(self.startWindow, text=" Enter Name:").grid(row=0, column=0)
        playerName = tk.Entry(self.startWindow, textvariable=self.playerName).grid(row=0, column=1)
        tk.Button(self.startWindow, text="Start", command=self.startGame).grid(row=0, column=2)

 
    def startGame(self):
        playerName = self.playerName.get()
        print(playerName)
        self.isActive = True
        self.startWindow.destroy()
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=0, column=0)
        togoforLabel = tk.Label(self.frame2, text="To Go For:")
        togoforLabel.grid(row=0, column=0, sticky='nsew')
        numberLabel = tk.Label(self.frame2, textvariable=self.goFor)
        numberLabel.grid(row=1, column=0, sticky='nsew')
        hitLabel = tk.Label(self.frame2, text="Enter Number Hit:")
        hitLabel.grid(row=0, column=1)
        self.hitCombo = ttk.Combobox(self.frame2, width = 15)
        self.hitCombo.grid(row=1, column=1, sticky='nsew')
        self.hitCombo['values'] = (0, 1, 2, 3,4,5,6, 7,8,9)
        #self.hitCombo.bind('<<ComboboxSelected>>', self.score_entered)
        self.hitCombo.bind('<Return>', self.score_entered)
        scoreButton = tk.Button(self.frame2, text=" Enter: ", command=self.score_entered)
        scoreButton.grid(row=2, column=1)
         
        totalLabel = tk.Label(self.frame2, text="Running Total : ")
        totalLabel.grid(row=0, column=2, sticky='nsew')
        runningLabel = tk.Label(self.frame2, textvariable=self.running)
        runningLabel.grid(row=1, column=2, sticky='nsew')
 
 
    def score_entered(self):
        score = int(self.hitCombo.get())
        subTotal = score * self.toGoFor
        self.runningTotal += subTotal
        self.toGoFor += 1
        if self.toGoFor == 21:
            self.toGoFor = 25
        if self.toGoFor == 5:
            self.running.set(self.runningTotal)
            self.gameFinished()
        else:
            self.goFor.set(self.toGoFor)
            self.running.set(self.runningTotal)
         
            self.hitCombo.set('')

 
class Finish(tk.Frame):
    def __init__(self):
        self.isActive = False
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Finish Page', bg='tomato')
        label.grid(column=0, row=0, sticky='news')


    def start(self):
        startWindow = tk.Toplevel()
 

class Main(tk.Frame):
    ''' Main class is the start/landing page '''
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Main Page', bg='gold')
        label.grid(column=0, row=0, sticky='news')
 

class HighScore(tk.Frame):
    '''
        HighScores class displays all scores
    '''
    def __init__(self):
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
        self.page2 = Rtb()
        self.page2.grid(column=0, row=0, sticky='news')
        self.page2.grid_columnconfigure(0, weight=3)
        self.page2.grid_rowconfigure(0, weight=3)
 
        page3 = Finish()
        page3.grid(column=0, row=0, sticky='news')
        page3.grid_columnconfigure(0, weight=3)
        page3.grid_rowconfigure(0, weight=3)
 
        page4 = HighScore()
        page4.grid(column=0, row=0, sticky='news')
        page4.grid_columnconfigure(0, weight=3)
        page4.grid_rowconfigure(0, weight=3)

        page1 = Main()
        page1.grid(column=0, row=0, sticky='news')
        page1.grid_columnconfigure(0, weight=3)
        page1.grid_rowconfigure(0, weight=3)
 
        
 
        # Setup the menus and commands
        game_menu = tk.Menu(self.window.menubar, tearoff=0)
        game_menu.add_command(label='501', command=page1.tkraise)
        game_menu.add_command(label='RTB', command=lambda: self.isGameActive( self.page2))
        game_menu.add_command(label='Finishes', command=page3.tkraise)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        page_menu = tk.Menu(self.window.menubar, tearoff=0)
        page_menu.add_command(label='501', command=page1.tkraise)
        page_menu.add_command(label='RTB ', command=lambda: self.isGameActive( self.page2))
        page_menu.add_command(label='Finishes', command=lambda: self.isGameActive( page3))
        page_menu.add_command(label='High Scores', command=page4.tkraise)
 
        page_menu.add_separator()
        page_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        self.window.menubar.add_cascade(label='New Game', menu=game_menu)
        self.window.menubar.add_cascade(label='High Scores', menu=page_menu)
 
    def isGameActive(self, page):
        page = page
        if page.isActive == False:
            page.tkraise()
            page.start()
        else:
            answer = messagebox.askyesnocancel("Question", "Game already in progress Continue playing?")
            if answer == True:
                page.tkraise()
            else:
                page.tkraise()
                page.start()



            
        
        
            

    
    
 
 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400+300+300')
    controller = Controller(Database(), Window(root))
    root.mainloop()