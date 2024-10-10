
from tkinter import *
import tkinter as tk
from tkinter import ttk
from database import Database
import sqlite3 as sq
import os


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

class Main(tk.Frame):
    ''' Main class is the start/landing page '''
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text='Main Page', bg='gold')
        label.grid(column=0, row=0, sticky='news')



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
 
        '''
        self.page3 = RoundTheBoard()
        self.page3.grid(column=0, row=0, sticky='news')
        self.page3.grid_columnconfigure(0, weight=3)
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
        #page6.grid_rowconfigure(0, weight=3
        )'''

        self.page1 = Main()
        self.page1.grid(column=0, row=0, sticky='news')
        self.page1.grid_columnconfigure(0, weight=3)
        self.page1.grid_rowconfigure(0, weight=3)

 
        
 
        # Setup the menus and commands
        game_menu = tk.Menu(self.window.menubar, tearoff=0)
        game_menu.add_command(label='501', command=self.page2.tkraise)
        #game_menu.add_command(label='Round the Board', command=self.page3.tkraise)
        #game_menu.add_command(label='Finishes', command=page4.tkraise)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        score_menu = tk.Menu(self.window.menubar, tearoff=0)
        score_menu.add_command(label='501 Averages', command=lambda: self.newGame(self.page1))
        #score_menu.add_command(label='Round the Board', command=self.page3.tkraise)
        #score_menu.add_command(label='Finishes', command=self.page3.tkraise)
        #score_menu.add_command(label='High Scores', command=self.page5.tkraise)
 
        #page_menu.add_separator()
        #page_menu.add_command(label='Exit', command=self.window.parent.destroy)
 
        self.window.menubar.add_cascade(label='New Game', menu=game_menu)
        self.window.menubar.add_cascade(label='High Scores', menu=score_menu)


        #self.page3.button['command'] = self.page1.tkraise

    def frame_destroy(self):
        self.page1.tkraise
        self.page3.frame3.destroy()

        

    #def newGame(self, page):
        #page = page
        #if page == self.page1:
            #self.page1.tkraise()
        #elif page == self.page2:
            #self.page2.tkraise()
 
    
 
 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x600+300+300')
    controller = Controller(Database(), Window(root))
    cwd = os.getcwd()
    print(cwd)
    root.mainloop()