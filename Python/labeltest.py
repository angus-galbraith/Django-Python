import tkinter as tk
from tkinter import ttk

plname = "Gus"
root = tk.Tk()

def changeName():
    plname = "Emma"
    nameLabel = tk.Label(root, text=plname)
    nameLabel.pack()
    print("Name changed")
    print(plname)

nameLabel = tk.Label(root, text=plname)
nameLabel.pack()

changeButton = tk.Button(root, text="Change", command=changeName)
changeButton.pack()






if __name__ == '__main__':
    
    root.geometry('600x400+300+300')
    
    root.mainloop()