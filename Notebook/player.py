from main import *
import tkinter as tk
from tkinter import ttk


#player class
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
        #game.player_to_throw()

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
        #if self.stats['legs'] == game.legs_to_win:
            #self.set_won()
        #else:
            #game.leg_to_play += 1
            #game.to_throw()
        

    def set_won(self):
        print('at sets')
        self.stats['sets'] += 1
        #if self.stats['sets'] == game.sets_to_win:
            #self.game_won()
        #else:
            #game.player1.stats['legs'] = 0
            #game.player2.stats['legs'] = 0
            #game.leg_to_play = 1
            #game.set_to_play += 1
            #game.to_throw()




    def game_won(self):
        print("Game over")
        
