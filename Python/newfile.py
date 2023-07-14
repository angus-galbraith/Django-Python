import tkinter as tk
 
 
class Page(tk.Frame):
    """A frame to be displayed in a stacked frame."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="news")
        self.connection = None
 
    def connect(self, function):
        """Provide a callback for the page."""
        self.connection = function
 
    def show(self):
        """Display this page."""
        self.tkraise()
 
 
class Game(Page):
    """Pretend game.  Enter your score and press button"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        font = (None, 24)
        self.name = tk.StringVar(self, "")
        self.score = tk.StringVar(self, "")
        name_label = tk.Label(self, text="Name", font=font)
        score_label = tk.Label(self, text="Score", font=font)
        name_entry = tk.Entry(self, textvariable=self.name, width=10, font=font)
        score_entry = tk.Entry(self, textvariable=self.score, width=4, font=font)
        button = tk.Button(self, text="Enter Score", font=font, command=self.game_over)
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        score_label.grid(row=1, column=0, padx=5, pady=5)
        score_entry.grid(row=1, column=1, padx=5, pady=5)
        button.grid(row=2, column=0, columnspan=2)
 
    def game_over(self):
        """Button callback.  Calls connection."""
        if self.connection:
            self.connection(self.name.get(), int(self.score.get()))
 
    def show(self):
        """Reset entries and display."""
        self.name.set("")
        self.score.set("")
        super().show()
 
 
class HighScore(Page):
    """Page that displays high score table."""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.scores = [tk.StringVar(self, "") for _ in range(10)]
        bg = self["bg"]
        label = tk.Label(self, text="High Scores", bg=bg, font=(None, 24))
        label.grid(row=0, column=0)
        for row, score in enumerate(self.scores, start=1):
            label = tk.Label(self, textvariable=score, width=20, bg=bg, font=(None, 20))
            label.grid(row=row, column=0)
        button = tk.Button(
            self, text="Play Again?", bg=bg, command=self.play_again, font=(None, 20)
        )
        button.grid(row=row, column=0, padx=5, pady=5)
 
    def play_again(self):
        """Called when play again button pressed."""
        if self.connection:
            self.connection()
 
    def show(self, high_scores):
        """Update scores and display."""
        for var in self.scores:
            var.set("")
        for (score, name), var in zip(high_scores, self.scores):
            var.set(f"{name:14} {score:5}")
        super().show()
 
 
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.high_scores = [(123, "Jimbo"), (950, "Billy"), (593, "Sassy")]
        pages = tk.Frame(self)
        pages.pack(expand=True, fill=tk.BOTH)
        self.game = Game(pages)
        self.game.connect(self.game_over)
        self.high_score = HighScore(pages)
        self.high_score.connect(self.game.show)
        self.game.show()
 
    def game_over(self, name, score):
        self.high_scores.append((score, name))
        self.high_scores = sorted(self.high_scores, reverse=True)[:10]
        self.high_score.show(self.high_scores)
 
 
if __name__ == "__main__":
    MainWindow().mainloop()