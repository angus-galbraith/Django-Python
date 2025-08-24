
import tkinter as tk
from tkinter import ttk
import sqlite3 as sq
import os
from player import *



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
    