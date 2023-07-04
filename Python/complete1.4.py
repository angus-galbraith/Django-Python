'''
This version will 501 as well. 
Menu items will be new game with drop down for each game, 
and High Scores with drop down for each game also for a player.
'''

from tkinter import *
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
        self.cursor.execute('''
            create table if not exists fiveohone (
            playername text, average integer, checkout integer
            )
        ''')
        self.connection.commit()
 
 
    def insert(self, playername, score, table):
        self.cursor.execute(f'insert into {table} (playername, score) values(?,?)', (playername, score))
        self.connection.commit()

    def insert_darts(self, playername, average, checkout, table):
        self.cursor.execute(f'insert into {table} (playername, average, checkout) values(?,?,?)', (playername, average, checkout))
        self.connection.commit()
        
             
    def getall(self, table):
        query = self.cursor.execute(f'select * from {table} order by score desc').fetchall()
        print(query)
        return query
 

class FiveOhOne(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

        #variables
        self.player1Name = tk.StringVar()
        self.player2Name = tk.StringVar()
        self.leg_to_play = 0
        self.set_to_play = 0
        

        frame1 = tk.Frame(self)
        frame1.grid(row=0)
        name1label = tk.Label(frame1, text="Player Name 1: ")
        name1label.grid(row=0, column=0, padx=10, pady=10)
        self.name1Entry = tk.Entry(frame1, textvariable=self.player1Name)
        self.name1Entry.grid(row=0, column=1)
        name2label = tk.Label(frame1, text="Player Name 2: ")
        name2label.grid(row=0, column=2, padx=10, pady=10)
        self.name2Entry = tk.Entry(frame1, textvariable=self.player2Name)
        self.name2Entry.grid(row=0, column=3)
        tk.Label(frame1, text="Sets: First to:-").grid(row=1, column=0)
        self.sets_spinbox = tk.Spinbox(frame1, values=(1,2,3,4))
        self.sets_spinbox.grid(row=1, column=1)
        tk.Label(frame1, text="Legs: First to:-").grid(row=1, column=2)
        self.legs_spinbox = tk.Spinbox(frame1, values=(1,2,3,4))
        self.legs_spinbox.grid(row=1, column=3)
        tk.Button(frame1, text="Start", command=self.start_game).grid(row=1, column=4)
        
        #
        #startButton.grid(row=0, column=4)


    
    def add_frames(self):
       self.frame_one = tk.Frame(self.game_frame)
       self.frame_one.grid(row=0, column=0)
       self.frame_three = tk.Frame(self.game_frame)
       self.frame_three.grid(row=0, column=1)
       self.frame_two = tk.Frame(self.game_frame)
       self.frame_two.grid(row=0, column=2)

    

    def start_game(self):
        self.game_frame = tk.Frame(self)
        self.game_frame.grid(row=1, column=0)
        self.legs_to_win = int(self.legs_spinbox.get()) # set variables for legs and sets 
        self.sets_to_win = int(self.sets_spinbox.get())
        self.player1 = player(self.legs_to_win)  #create 2 instances of the player class
        self.player2 = player(self.legs_to_win)
        self.player1.stats["name"]= self.player1Name.get()  # set the players names
        self.player2.stats["name"] = self.player2Name.get()
        self.add_frames()
        self.name1Entry.configure(bg="lightblue")
        self.name2Entry.configure(bg="lightblue")
        self.screen_refresh(self.frame_one, self.frame_two, self.frame_three, self.player1.stats, self.player2.stats) # populate the three screens
        
       
        
        self.to_throw()

    
    

    def screen_refresh(self, frame, frame1, frame2, player, player1):
        player = player
        frame = frame
        rownum = 0
        for (key, value) in player.items():
            tk.Label(frame, text=key).grid(row=rownum, column=0)
            tk.Label(frame, text=value).grid(row=rownum, column=1)
            rownum += 1
        player1 = player1
        frame1 = frame1
        rownum = 0
        for (key, value) in player1.items():
            tk.Label(frame1, text=key).grid(row=rownum, column=0)
            tk.Label(frame1, text=value).grid(row=rownum, column=1)
            rownum += 1
        frame2 = frame2
        tk.Label(frame2, text=self.player1.stats["name"], font=(None, 25)).grid(row=0, column=0)
        tk.Label(frame2, text=self.player2.stats["name"], font=(None, 25)).grid(row=0, column=1)
        self.pl1_remaining = tk.Label(frame2, text=self.player1.score["remaining"], font=(None, 40), width=3, height=1)
        self.pl1_remaining.grid(row=1, column=0)
        self.pl1_remaining.configure(bg="white")
        self.pl2_remaining = tk.Label(frame2, text=self.player2.score["remaining"], font=(None, 40), width=3, height=1)
        self.pl2_remaining.grid(row=1, column=1)
        self.pl2_remaining.configure(bg="white")
        self.score_ent = tk.Entry(frame2, width=10)
        self.score_ent.grid(row=2,column=0)
        tk.Button(frame2, text="Enter Score", command=self.button_pressed).grid(row=2, column=1)


    def to_throw(self): # called on al the start of a  leg
        self.player1.score['remaining'] = 501
        self.player2.score['remaining'] = 501
        self.screen_refresh(self.frame_one, self.frame_two, self.frame_three, self.player1.stats, self.player2.stats)
        if self.set_to_play % 2 != 0:
            if self.leg_to_play %2 != 0:
                self.current_player = 1
                self.player_to_throw()
            else:
                self.current_player = 2
                self.player_to_throw()
        else:
            if self.leg_to_play %2 != 0:
                self.current_player = 2
                self.player_to_throw()
            else:
                self.current_player = 1
                self.player_to_throw()


    def player_to_throw(self): # callled for each throw
        if self.current_player == 1:
            self.screen_refresh(self.frame_one, self.frame_two, self.frame_three, self.player1.stats, self.player2.stats)
            self.pl1_remaining.configure(bg="yellow")
            self.pl2_remaining.configure(bg="white")
            self.score_ent.focus()
        else:
            self.screen_refresh(self.frame_one, self.frame_two, self.frame_three, self.player1.stats, self.player2.stats)
            self.pl2_remaining.configure(bg="yellow")
            self.pl1_remaining.configure(bg="white")
            self.score_ent.focus()
        



    def button_pressed(self):
        score = int(self.score_ent.get())
        if self.current_player == 1:
            self.current_player = 2
            self.player1.score_entered(score)
            self.player_to_throw()

        else:
            self.current_player = 1
            self.player2.score_entered(score)
            self.player_to_throw()



        


class player():
    def __init__(self, legs_to_win):
        self.legs_to_win = legs_to_win

        self.name = "Player"
        
        self.stats = {
            "name": "Player",
            "sets": 0,
            "legs": 0,
            "180": 0,
            "160": 0,
            "140": 0,
            "120": 0,
            "100": 0,
            "80": 0,
            "60": 0,
            "Average": 0,
            "Darts at double": 0,
            "Doubles Hit": 0,
            "Checkout %": 0,
            
        }

        self.score = {
            "remaining": 501,
            "totalscore": 0,
            "totaldarts": 0,
            
        }

    def score_entered(self, score):
        score = score
        self.score['remaining'] -= score
        self.score['totalscore'] += score
        if score == 180:
            self.stats['180'] += 1
        elif score >= 160:
            self.stats['160'] += 1
        elif score >= 140:
            self.stats['140'] += 1
        elif score >= 120:
            self.stats['120'] += 1
        elif score >= 100:
            self.stats['100'] += 1
        elif score >= 80:
            self.stats['80'] += 1
        elif score >= 60:
            self.stats['60'] += 1
        
        if self.score['remaining'] == 0:
            self.leg_won()
        elif self.score['remaining'] <= 50:
            self.darts_at_double()
        
        self.score['totaldarts'] += 3
        self.calculate_averages()

        
        return

    def darts_at_double(self):
        self.doubles_window = tk.Toplevel()
        tk.Label(self.doubles_window, text="Number of Darts at Doubles").grid(row=0, column=0)
        self.darts_doubles = tk.Spinbox(self.doubles_window, values=(0,1,2,3))
        self.darts_doubles.grid(row=0, column=1)
        tk.Button(self.doubles_window, text="Enter ", command=self.doubles_button_pressed).grid(row=1, column=1, columnspan=2)
        self.doubles_window.attributes('-topmost', 'true')
        

    def doubles_button_pressed(self):
        at_doubles = int(self.darts_doubles.get())
        self.stats['Darts at double'] += at_doubles
        self.doubles_window.destroy()
        controller.page2.player_to_throw()

    def calculate_averages(self):
        self.stats['Average'] = round(3*(self.score['totalscore']/self.score['totaldarts']), 1)
        
    def leg_won(self):
        self.leg_window = tk.Toplevel()
        tk.Label(self.leg_window, text="Number of Darts Used").grid(row=0, column=0)
        self.darts_used = tk.Spinbox(self.leg_window, values=(0,1,2,3))
        self.darts_used.grid(row=0, column=1)
        tk.Label(self.leg_window, text="Number of Darts at Doubles").grid(row=1, column=0)
        self.darts_doubles = tk.Spinbox(self.leg_window, values=(0,1,2,3))
        self.darts_doubles.grid(row=1, column=1)
        tk.Button(self.leg_window, text='Enter', command=self.leg_button_pressed).grid(row=2, column=1, columnspan=2)
        self.leg_window.attributes('-topmost', 'true')

    def leg_button_pressed(self):
        self.stats['legs'] += 1
        self.stats['Doubles Hit'] += 1
        doubledarts = int(self.darts_doubles.get())
        self.stats['Darts at double'] += doubledarts
        self.stats["Checkout %"] = (self.stats['Doubles Hit']/self.stats['Darts at double'])*100
        
        totaldarts = int(self.darts_used.get())
        self.score['totaldarts'] += totaldarts
        self.leg_window.destroy()
        if self.stats['legs'] == self.legs_to_win:
            self.set_won()
        else:
            controller.page2.leg_to_play += 1
            controller.page2.to_throw()
        

    def set_won(self):
        print('at sets')
        self.stats['sets'] += 1
        if self.stats['sets'] == controller.page2.sets_to_win:
            self.game_won()
        else:
            controller.page2.player1.stats['legs'] = 0
            controller.page2.player2.stats['legs'] = 0
            controller.page2.leg_to_play = 1
            controller.page2.set_to_play += 1
            controller.page2.to_throw()




    def game_won(self):
        print("Game over")
        
        controller.db.insert_darts(controller.page2.player1.stats["name"], controller.page2.player1.stats["Average"], controller.page2.player1.stats["Checkout %"], "fiveohone" )
        print("Database updated")
        #player_stats.update_stats()


 
class RoundTheBoard(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        #label = tk.tk.Label(self, text='Rtb Page', bg='pink')
        #label.grid(column=0, row=0, sticky='news')
 
        #variables
        self.playerName = tk.StringVar()
        self.toGoFor = 1
        self.runningTotal = 0
        self.goFor = tk.IntVar()
        self.goFor.set(self.toGoFor)
        self.running = tk.IntVar()
        self.running.set(self.runningTotal)
         
 
 
        frame1 = tk.Frame(self)
        frame1.grid(row=0)
        namelabel = tk.Label(frame1, text="Player Name: ")
        namelabel.grid(row=0, column=0, padx=10, pady=10)
        nameEntry = tk.Entry(frame1, textvariable=self.playerName)
        nameEntry.grid(row=0, column=1)
        startButton = tk.Button(frame1, text="Start", command=self.show_frame2)
        startButton.grid(row=0, column=2)
 
    def show_frame2(self):
        self.name = self.playerName.get()
        frame2 = tk.Frame(self)
        frame2.grid(row=1, column=0)
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
         
 
class Main(tk.Frame):
    ''' Main class is the start/landing page '''
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Main Page', bg='gold')
        label.grid(column=0, row=0, sticky='news')
 
 
class Finishes(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        
        #variables
        self.toGoFor = 61
        self.runningTotal = 0
        self.goFor = tk.IntVar()
        self.goFor.set(self.toGoFor)
        self.running = tk.IntVar()
        self.running.set(self.runningTotal)
        self.playerName = tk.StringVar()
 
        #create frame one, get the name and call frame 2 
        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0)
        namelabel = tk.Label(frame1, text="Player Name: ")
        namelabel.grid(row=0, column=0)
        nameEntry = tk.Entry(frame1, textvariable=self.playerName)
        nameEntry.grid(row=0, column=1)
        startButton = tk.Button(frame1, text="Start", command=self.show_frame2)
        startButton.grid(row=0, column=2)
 
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
         
 
 
class HighScores(tk.Frame):
    '''
        HighScores class displays all scores
    '''
    def __init__(self,):
        tk.Frame.__init__(self)
        
        #create frames
        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0)
        frame2 = tk.Frame(self)
        frame2.grid(row=1, column=0)
        frame3 = tk.Frame(self)
        frame3.grid(row=1, column=1)
        frame4 = tk.Frame(self)
        frame4.grid(row=1, column=2)

        # buttons
        rtbButton = tk.Button(frame1, text="Round the Board", command=self.showRtbFrame)
        rtbButton.grid(row=0, column=0)
        finishesButton = tk.Button(frame1, text="Finishes", command=self.showRtbFrame)
        finishesButton.grid(row=0, column=1)
        averageButton = tk.Button(frame1, text="Darts - Average", command=self.showRtbFrame)
        averageButton.grid(row=0, column=2)
        checkButton = tk.Button(frame1, text="Darts - Checkout%", command=self.showRtbFrame)
        checkButton.grid(row=0, column=3)


    def showRtbFrame(self):
        rtblist = controller.db.getall("rtbhigh")
        print(rtblist)





 
 
class NewGame(tk.Frame):
    ''' NewGame class page for starting new games '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        frame2 = tk.Frame(self)
        frame2.grid(row=1, column=0, sticky='nsew')
        label = tk.Label(frame1, text='Start a new game', bg='burlywood')
        #label['font'] = (None, 16, 'normal')
        label.grid(column=0, row=0, sticky='nsew')
        
        fiveOhOneButton = tk.Button(frame2, text=" 501 ", command=self.darts)
        fiveOhOneButton.grid(row=0, column=0, sticky='nsew')
        rtbButton = tk.Button(frame2, text="Round the Board", command=self.rtb)
        rtbButton.grid(row=0, column=1, sticky='nsew')


    def darts(self):
        pass


    def rtb(self):
        pass
 
 
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
        

        self.page2 = FiveOhOne()
        self.page2.grid(column=0, row=0, sticky='news')
        self.page2.grid_columnconfigure(0, weight=3)
        #page2.grid_rowconfigure(0, weight=3)
 
        page3 = RoundTheBoard()
        page3.grid(column=0, row=0, sticky='news')
        page3.grid_columnconfigure(0, weight=3)
        #page3.grid_rowconfigure(0, weight=3)
 
        page4 = Finishes()
        page4.grid(column=0, row=0, sticky='news')
        page4.grid_columnconfigure(0, weight=3)
        #page4.grid_rowconfigure(0, weight=3)
 
        self.page5 = HighScores()
        self.page5.grid(column=0, row=0, sticky='news')
        #page5.grid_columnconfigure(0, weight=3)
        #page5.grid_rowconfigure(0, weight=3)

        page6 = NewGame()
        page6.grid(column=0, row=0, sticky='news')
        #page6.grid_columnconfigure(0, weight=3)
        #page6.grid_rowconfigure(0, weight=3)

        self.page1 = Main()
        self.page1.grid(column=0, row=0, sticky='news')
        self.page1.grid_columnconfigure(0, weight=3)
        self.page1.grid_rowconfigure(0, weight=3)

 
        
 
        # Setup the menus and commands
        game_menu = tk.Menu(self.window.menubar, tearoff=0)
        game_menu.add_command(label='501', command=self.page2.tkraise)
        game_menu.add_command(label='Round the Board', command=page3.tkraise)
        game_menu.add_command(label='Finishes', command=page4.tkraise)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        score_menu = tk.Menu(self.window.menubar, tearoff=0)
        score_menu.add_command(label='501 Averages', command=lambda: self.newGame(self.page1))
        score_menu.add_command(label='Round the Board', command=page3.tkraise)
        score_menu.add_command(label='Finishes', command=page3.tkraise)
        score_menu.add_command(label='High Scores', command=self.page5.tkraise)
 
        #page_menu.add_separator()
        #page_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        self.window.menubar.add_cascade(label='New Game', menu=game_menu)
        self.window.menubar.add_cascade(label='High Scores', menu=score_menu)

    #def newGame(self, page):
        #page = page
        #if page == self.page1:
            #self.page1.tkraise()
        #elif page == self.page2:
            #self.page2.tkraise()
 
    
 
 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400+300+300')
    controller = Controller(Database(), Window(root))
    root.mainloop()