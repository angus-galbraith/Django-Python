"""
This version works and the frames are callable from anywhere.
Datatbase doesnt show update at the time, all the database stuff is inside the __init__, which is the likely
reason for the issue.
"""
import tkinter as tk
from tkinter import ttk
import sqlite3
 
 
class practice(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")
 
        # creating a frame and assigning it to container
        container = tk.Frame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)
 
        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
 
        self.menu = tk.Menu(container, bg="lightgrey", fg="black")
        # first menu item
        self.game_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.game_menu.add_command(label="New Game", command=lambda: self.show_frame("RtbPage"))
        self.menu.add_cascade(label="Round the board", menu=self.game_menu)
 
        # second menu item
        self.stat_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.stat_menu.add_command(label="New Game", command=lambda: self.show_frame("FinishesPage"))
        self.menu.add_cascade(label="Finishes", menu=self.stat_menu)
 
        # third menu item
        self.stat_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.stat_menu.add_command(label="High Scores", command=lambda: self.show_frame("HighScoresPage"))
        self.menu.add_cascade(label="High Scores", menu=self.stat_menu)
 
        # populate the menu
        self.config(menu=self.menu)

        self.db_connect()
 
     # We will now create a dictionary of frames
        self.frames = {}
        for F in (StartPage, RtbPage, FinishesPage, HighScoresPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        
        self.show_frame("StartPage")
        
 
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()
 
    def db_connect(self):
        connection = sqlite3.connect('highscores.db')
        cur = connection.cursor()
 
        
        cur.execute(f''' CREATE TABLE  if not exists rtbhigh(playername text, score integer) ''')
        cur.execute(f''' CREATE TABLE if not exists finisheshigh(playername text, score integer) ''')
 
        connection.commit()
        

   
   
 
 
 
 
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Main Page")
        label.pack(padx=10, pady=10)
 
 
class RtbPage(tk.Frame):
    def __init__(self, parent, controller   ):
        tk.Frame.__init__(self, parent)
 
        #variables
        self.playerName = tk.StringVar()
        self.toGoFor = 1
        self.runningTotal = 0
        self.goFor = tk.IntVar()
        self.goFor.set(self.toGoFor)
        self.running = tk.IntVar()
        self.running.set(self.runningTotal)
         
 
 
        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        namelabel = tk.Label(frame1, text="Player Name: ")
        namelabel.grid(row=0, column=0, sticky='ew')
        nameEntry = tk.Entry(frame1, textvariable=self.playerName)
        nameEntry.grid(row=0, column=1, sticky='ew')
        startButton = tk.Button(frame1, text="Start", command=self.show_frame2)
        startButton.grid(row=0, column=2, sticky='ew')
 
    def show_frame2(self):
        self.name = self.playerName.get()
        frame2 = tk.Frame(self)
        frame2.grid(row=1, column=0, sticky='nsew')
        togoforLabel = tk.Label(frame2, text="To Go For:")
        togoforLabel.grid(row=0, column=0, sticky='nsew')
        numberLabel = tk.Label(frame2, textvariable=self.goFor)
        numberLabel.grid(row=1, column=0, sticky='nsew')
        hitLabel = tk.Label(frame2, text="Enter Number Hit:")
        hitLabel.grid(row=0, column=1)
        self.hitCombo = ttk.Combobox(frame2, width = 15)
        self.hitCombo.grid(row=1, column=1, sticky='nsew')
        self.hitCombo['values'] = (0, 1, 2, 3,4,5,6, 7,8,9)
        #self.hitCombo.bind('<<ComboboxSelected>>', self.score_entered)
        self.hitCombo.bind('<Return>', self.score_entered)
        scoreButton = tk.Button(frame2, text=" Enter: ", command=self.score_entered)
        scoreButton.grid(row=2, column=1)
         
        totalLabel = tk.Label(frame2, text="Running Total : ")
        totalLabel.grid(row=0, column=2, sticky='nsew')
        runningLabel = tk.Label(frame2, textvariable=self.running)
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
         
 
    def gameFinished(self):
        frame3 = tk.Frame(self)
        frame3.grid(row=2, column=0, sticky='nsew')
        overLabel = tk.Label(frame3, text="Game Over: Your Total is: ")
        overLabel.grid(row=0, column=0, sticky='nsew')
        totalLabel = tk.Label(frame3, textvariable=self.running)
        totalLabel.grid(row=0, column=1, sticky='nsew')
        saveButton = tk.Button(frame3, text="Save", command=self.addToDb)
        saveButton.grid(row=0, column=2, sticky='nsew')
 
    def addToDb(self):
        name = self.name
        total = self.runningTotal
         
        connection = sqlite3.connect('highscores.db')
        cur = connection.cursor()
 
        insert_statement = ''' INSERT INTO rtbhigh(playername, score) VALUES(?, ?); '''
        insert_values = (name, total)
 
         
        cur.execute(insert_statement, insert_values)
        print("done")
             
 
        connection.commit()
        
         
 
 
class FinishesPage(tk.Frame,):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
 
        #variables
        self.toGoFor = 61
        self.runningTotal = 0
        self.goFor = tk.IntVar()
        self.goFor.set(self.toGoFor)
        self.running = tk.IntVar()
        self.running.set(self.runningTotal)
        self.playerName = tk.StringVar()
 
 
        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        namelabel = tk.Label(frame1, text="Player Name: ")
        namelabel.grid(row=0, column=0, sticky='ew')
        nameEntry = tk.Entry(frame1, textvariable=self.playerName)
        nameEntry.grid(row=0, column=1, sticky='ew')
        startButton = tk.Button(frame1, text="Start", command=self.show_frame2)
        startButton.grid(row=0, column=2, sticky='ew')
 
    def show_frame2(self):
        self.name = self.playerName.get()
        frame2 = tk.Frame(self)
        frame2.grid(row=1, column=0, sticky='nsew')
        togoforLabel = tk.Label(frame2, text="To Go For:")
        togoforLabel.grid(row=0, column=0, sticky='nsew')
        numberLabel = tk.Label(frame2, textvariable=self.goFor)
        numberLabel.grid(row=1, column=0, sticky='nsew')
        hitLabel = tk.Label(frame2, text="Number of darts used:")
        hitLabel.grid(row=0, column=1)
        self.hitCombo = ttk.Combobox(frame2, width = 15)
        self.hitCombo.grid(row=1, column=1, sticky='nsew')
        self.hitCombo['values'] = (2,3,4,5,6,0)
        self.hitCombo.bind('<<ComboboxSelected>>')
        scoreButton = tk.Button(frame2, text=" Enter: ", command=self.score_entered)
        scoreButton.grid(row=2, column=1)
        totalLabel = tk.Label(frame2, text="Running Total : ")
        totalLabel.grid(row=0, column=2, sticky='nsew')
        runningLabel = tk.Label(frame2, textvariable=self.running)
        runningLabel.grid(row=1, column=2, sticky='nsew')
 
 
    def score_entered(self):
        darts = int(self.hitCombo.get())
        if self.toGoFor == 99:
            if darts == 0:
                self.runningTotal += 0
            elif darts == 3:
                self.runningTotal += 3
            elif darts == 4 or 5 or 6:
                self.runningTotal += 1
             
        else:
            if darts == 0:
                self.runningTotal += 0
            elif darts == 2:
                self.runningTotal += 3
            elif darts == 3:
                self.runningTotal += 2
            elif darts == 4 or 5 or 6:
                self.runningTotal += 1
            self.running.set(self.runningTotal)
            self.toGoFor += 1
            if self.toGoFor == 63:
                self.gameFinished()
            else:
                self.goFor.set(self.toGoFor)
                self.hitCombo.set('')
         
 
    def gameFinished(self):
        frame3 = tk.Frame(self)
        frame3.grid(row=2, column=0, sticky='nsew')
        overLabel = tk.Label(frame3, text="Game Over: Your Total is: ")
        overLabel.grid(row=0, column=0, sticky='nsew')
        tk.Label(frame3, text=self.runningTotal).grid(row=0,column=1, sticky='nsew')
        saveButton = tk.Button(frame3, text="Save", command=self.addToDb)
        saveButton.grid(row=0, column=2, sticky='nsew')
 
    def addToDb(self):
        name = self.name
        total = self.runningTotal
         
        connection = sqlite3.connect('highscores.db')
        cur = connection.cursor()
 
        insert_statement = ''' INSERT INTO finisheshigh(playername, score) VALUES(?, ?); '''
        insert_values = (name, total)
 
         
        cur.execute(insert_statement, insert_values)
        print("done")
             
 
        connection.commit()
        read_query = '''SELECT * FROM finisheshigh'''
        cur.execute(read_query)
        items = cur.fetchall()
        print(items)
        
        game.show_frame("HighScoresPage")
 
         
 
         
 
 
     
 
 
 
class HighScoresPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        frame2 = tk.Frame(self)
        frame2.grid(row=0, column=1, sticky='nsew')
 
        connection = sqlite3.connect('highscores.db')
        cur = connection.cursor()
        #connection.commit()
        # populate rtb table
        read_query = '''SELECT * FROM rtbhigh ORDER BY score DESC'''
        cur.execute(read_query)
        items = cur.fetchall()
 
        tk.Label(frame1, text="Round the board").grid(row=0,column=0, columnspan=3)
 
        row = 1
        buttonnumber = 1 
         
        for item in items:
            fullframe = tk.Frame(frame1, highlightbackground="black", highlightthickness=1)
            fullframe.grid(row=row, column=0)
            tk.Label(fullframe, text=buttonnumber).grid(row=0, column=0)
            tk.Label(fullframe, text=item[0], width=20).grid(row=0, column=1)
            tk.Label(fullframe, text=item[1]).grid(row=0, column=2)
            row += 1 
            buttonnumber +=1
 
        #populate finishes table
        read_query = '''SELECT * FROM finisheshigh ORDER BY score DESC'''
        cur.execute(read_query)
        items = cur.fetchall()
        print(items)
 
        tk.Label(frame2, text="Finishes").grid(row=0,column=0, columnspan=3)
 
        row = 1
        buttonnumber = 1 
 
        for item in items:
            fullframe = tk.Frame(frame2, highlightbackground="black", highlightthickness=1)
            fullframe.grid(row=row, column=0)
            tk.Label(fullframe, text=buttonnumber).grid(row=row, column=0)
            tk.Label(fullframe, text=item[0], width=20).grid(row=row, column=1)
            tk.Label(fullframe, text=item[1]).grid(row=row, column=2)
            row += 1 
            buttonnumber +=1
 
        connection.commit()
        cur.close()
 
 
 
 
         
         
 
     
 
if __name__ == "__main__":
    game = practice()
    game.mainloop()