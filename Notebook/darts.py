import main
from player import *
import tkinter as tk
from tkinter import ttk




class darts(ttk.Frame):
    def __init__(self, container):
        super().__init__()
                
        self.game_frame = tk.Frame(self)
        self.game_frame.grid(row=0, column=0)
        self.player1 = player()
        self.player2 = player()
        self.add_frames()
        self.setup_screen()
        #self.new_game()
        
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
        self.pl1_entry = tk.Button(frame2, text="Enter Score", )
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
        
