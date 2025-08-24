
import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
import os



class player():
    def __init__(self):
        
        # stats for each player
        #these are used in a loop to populate the players frames

        self.stats = {
            "Name:-": "Player",
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
        game.player_to_throw()

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
        if self.stats['legs'] == game.legs_to_win:
            self.set_won()
        else:
            game.leg_to_play += 1
            game.to_throw()
        

    def set_won(self):
        print('at sets')
        self.stats['sets'] += 1
        if self.stats['sets'] == game.sets_to_win:
            self.game_won()
        else:
            game.player1.stats['legs'] = 0
            game.player2.stats['legs'] = 0
            game.leg_to_play = 1
            game.set_to_play += 1
            game.to_throw()




    def game_won(self):
        print("Game over")
        

# main class window
class FiveOhOne(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game_frame = tk.Frame(self)
        self.game_frame.grid(row=0, column=0)
        self.player1 = player()
        self.player2 = player()
        self.add_frames()
        self.setup_screen()
        self.new_game()
        
    #sets out the three main frames in the main window.
    def add_frames(self):
        self.frame_one = tk.Frame(self.game_frame)
        self.frame_one.grid(row=0, column=0)
        self.frame_three = tk.Frame(self.game_frame)
        self.frame_three.grid(row=0, column=1)
        self.frame_two = tk.Frame(self.game_frame)
        self.frame_two.grid(row=0, column=2)

     #displays the inital screen
     # keeps the entry buttons outwith screen refresh as they are static.  
    def setup_screen(self):
        self.screen_refresh()
        frame2 = self.frame_three
        self.pl1_entry = tk.Button(frame2, text="Enter Score", command=self.button_pressed)
        self.score_ent = tk.Entry(frame2, width=5)
        self.score_ent.grid(row=2,column=0, columnspan=2)
        self.pl1_entry.grid(row=3, column=0, columnspan=2)
        
        

    
    # populates the three frames. can be called anytime the stats cha
    def screen_refresh(self):

        player1 = self.player1.stats
        frame = self.frame_one
        rownum = 0
        for (key, value) in player1.items():
            tk.Label(frame, text=key).grid(row=rownum, column=0)
            tk.Label(frame, text=value).grid(row=rownum, column=1)
            rownum += 1
        player2 = self.player2.stats
        frame1 = self.frame_two
        rownum = 0
        for (key, value) in player2.items():
            tk.Label(frame1, text=key).grid(row=rownum, column=0)
            tk.Label(frame1, text=value).grid(row=rownum, column=1)
            rownum += 1
        frame2 = self.frame_three
        tk.Label(frame2, text=self.player1.stats["Name:-"], font=(None, 25)).grid(row=0, column=0)
        tk.Label(frame2, text=self.player2.stats["Name:-"], font=(None, 25)).grid(row=0, column=1)
        self.pl1_remaining = tk.Label(frame2, text=self.player1.score["remaining"], font=(None, 40), width=3, height=1)
        self.pl1_remaining.grid(row=1, column=0)
        self.pl1_remaining.configure(bg="white")
        self.pl2_remaining = tk.Label(frame2, text=self.player2.score["remaining"], font=(None, 40), width=3, height=1)
        self.pl2_remaining.grid(row=1, column=1)
        self.pl2_remaining.configure(bg="white")
        
        
        

    def new_game(self):
        self.win = tk.Toplevel()
        tk.Label(self.win, text="Player 1:").grid(row=0, column=0)
        self.pl1ent = tk.Entry(self.win)
        self.pl1ent.grid(row=0,column=1)
        tk.Label(self.win, text="Player 2:").grid(row=1, column=0)
        self.pl2ent = tk.Entry(self.win)
        self.pl2ent.grid(row=1,column=1)
        tk. Label(self.win, text="Sets: First to:-").grid(row=2, column=0)
        self.sets_spinbox = tk.Spinbox(self.win, values=(1,2,3,4))
        self.sets_spinbox.grid(row=2, column=1)
        tk.Label(self.win, text="Legs: First to:-").grid(row=3, column=0)
        self.legs_spinbox = tk.Spinbox(self.win, values=(1,2,3,4))
        self.legs_spinbox.grid(row=3, column=1)
        tk.Button(self.win, text="Start", command=self.start_game).grid(row=4, column=1,columnspan=2)

    def start_game(self):
        legs_to_win = int(self.legs_spinbox.get()) # set variables for legs and sets 
        sets_to_win = int(self.sets_spinbox.get())
        self.legs_to_win = legs_to_win/2 + 1 # once a leg is won the players total will be compared to this
        self.sets_to_win = sets_to_win/2 + 1 # once a set is won the players total will be compared to this
        self.player1.stats["Name:-"]= self.pl1ent.get()  # set the players names
        self.player2.stats["Name:-"] = self.pl2ent.get()
        self.leg_to_play = 0
        self.set_to_play = 0
        self.screen_refresh()
        self.to_throw()

    def to_throw(self): # called on al the start of a  leg
        self.player1.score['remaining'] = 501
        self.player2.score['remaining'] = 501
        self.screen_refresh()
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
            self.screen_refresh()
            self.pl1_remaining.configure(bg="yellow")
            self.pl2_remaining.configure(bg="white")
            self.score_ent.delete(0, tk.END)
            self.score_ent.focus()
        else:
            self.screen_refresh()
            self.pl2_remaining.configure(bg="yellow")
            self.pl1_remaining.configure(bg="white")
            self.score_ent.delete(0, tk.END)
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

if __name__ == "__main__":
    game = FiveOhOne()
    game.mainloop()
    