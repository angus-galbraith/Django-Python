import tkinter as tk
import sqlite3 as sq
 
class Database:
    '''
        Database class handles all database functions.
        Connects, creates, inserts, and get data
    '''
    def __init__(self):
        ''' Set some instance variables '''
        self.table = 'finisheshigh'
        self.connection = sq.connect('highscores.db')
        self.cursor = self.connection.cursor()
 
    def create(self):
        ''' Method for creating the table '''
        self.cursor.execute(f'''
            create table if not exists {self.table} (
            id integer primary key,
            playername text,
            score integer
            )
        ''')
        self.connection.commit()
 
    def insert(self, playername, score):
        ''' Method for inserting data '''
        self.cursor.execute(f'''
            insert into {self.table} (playername, score)
            values (?, ?)''', (playername, score))
        self.connection.commit()
 
    def getall(self):
        ''' Method for getting data '''
        self.cursor.execute(f'select * from {self.table} order by score desc')
        return self.cursor.fetchall()
     
 
class Window:
    '''
        Window class sets up the main window view
    '''
    def __init__(self, parent):
        self.parent = parent
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
 
        self.container = tk.Frame(parent)
        self.container.grid(column=0, row=0, sticky='news', padx=5, pady=5)
        self.container.grid_columnconfigure(0, weight=3, uniform='columns')
        self.container.grid_columnconfigure(1, weight=3, uniform='columns')
 
        header = tk.Label(self.container, text='Player', bg='lightgray')
        header['font'] = (None, 16, 'bold')
        header['relief'] = 'groove'
        header.grid(column=0, row=0, sticky='new', padx=(5,0), pady=(5,1))
 
        header2 = tk.Label(self.container, text='Score', bg='lightgray')
        header2['font'] = (None, 16, 'bold')
        header2['relief'] = 'groove'
        header2.grid(column=1, row=0, sticky='new', padx=(2,3), pady=(5,1))
 
        self.data_container = tk.Frame(self.container)
        self.data_container['relief'] = 'groove'
        self.data_container.grid(column=0, columnspan=2, row=1, sticky='new', padx=5, pady=(1,5))
        self.data_container.grid_columnconfigure(0, weight=3, uniform='columns')
        self.data_container.grid_columnconfigure(1, weight=3, uniform='columns')
        self.data_container.grid_columnconfigure(0, weight=3, uniform='data')
        self.data_container.grid_columnconfigure(1, weight=3, uniform='data')
 
        self.button = tk.Button(self.container, text='Add Entry')
        self.button['font'] = (None, 12, 'bold')
        self.button['cursor'] = 'hand2'
        self.button.grid(column=0, columnspan=2, row=3, ipadx=2, ipady=2)
 
 
class Form:
    ''' Form class builds and displays the form in a toplevel window '''
    def __init__(self, parent, getall):
        self.parent = parent
        self.getall = getall
        self.window = tk.Toplevel(None)
        self.window['padx'] = 10
        self.window['pady'] = 5
        self.window.title('Data Form')
 
        self.name = tk.StringVar()
        self.score = tk.StringVar()
 
        label = tk.Label(self.window, text='Name:', font=(None, 14, 'bold'))
        label.grid(column=0, row=0, sticky='new', pady=2)
        name = tk.Entry(self.window, textvariable=self.name, font=(None, 14, 'normal'))
        name.grid(column=1, row=0, sticky='new')
 
        label = tk.Label(self.window, text='Score:', font=(None, 14, 'bold'))
        label.grid(column=0, row=1, sticky='new', pady=2)
        score = tk.Entry(self.window, textvariable=self.score, font=(None, 14, 'normal'))
        score.grid(column=1, row=1, sticky='new')
 
        button = tk.Button(self.window, text='Submit', font=(None, 12, 'normal'))
        button['command'] = lambda: self.insert(self.name, self.score)
        button.grid(column=0, columnspan=2, row=2)
 
        self.window.protocol('WM_DELETE_WINDOW', self.close)
 
    def insert(self, name, score):
        ''' Method that inserts the data '''
        Database().insert(name.get(), score.get())
        self.close()
 
    def close(self):
        ''' A way to close the toplevel window and reopen the main window '''
        self.window.destroy()
        self.getall()
        self.parent.deiconify()
 
 
class Controller:
    '''
        Controller class communicates between the classes
    '''
    def __init__(self, database, window):
        # Set instance variables and populate the window if data exists
        self.database = database
        self.database.create()
        self.window = window
        self.getall()
 
        # Command for the window button to open toplevel window
        self.window.button['command'] = self._window
 
    def _window(self):
        ''' Method for withdrawing main window and opoening toplevel window '''
        self.window.parent.withdraw()
        form = Form(self.window.parent, self.getall)
 
    def getall(self):
        '''
         This method could be improved on
        '''
        stats = self.database.getall() # Get database entries
 
        # This will destroy and rebuild the data container in the main window.
        # Reasoning was that trace data was still visible after entering data
        self.window.data_container.destroy()
        self.window.data_container = tk.Frame(self.window.container)
        self.window.data_container['relief'] = 'groove'
        self.window.data_container.grid(column=0, columnspan=2, row=1, sticky='new', padx=5, pady=(1,5))
        self.window.data_container.grid_columnconfigure(0, weight=3, uniform='columns')
        self.window.data_container.grid_columnconfigure(1, weight=3, uniform='columns')
        self.window.data_container.grid_columnconfigure(0, weight=3, uniform='data')
        self.window.data_container.grid_columnconfigure(1, weight=3, uniform='data')
 
        # if there is no data display a message stating so else populate
        if not stats:
            label = tk.Label(self.window.data_container)
            label['text'] = 'Currently, there are not any stats recorded.'
            label['fg'] = 'red'
            label['font'] = (None, 14, 'normal')
            label['relief'] = 'ridge'
            label.grid(column=0, columnspan=2, row=0, sticky='new', ipadx=5)
        else:
            for row, data in enumerate(self.database.getall()):
                label = tk.Label(self.window.data_container)
                label['font'] = (None, 14, 'normal')
                label['text'] = data[0]
                label['relief'] = 'ridge'
                label.grid(column=0, row=row, sticky='new', padx=(0,1), pady=2)
 
                label = tk.Label(self.window.data_container)
                label['font'] = (None, 14, 'normal')
                label['text'] = data[1]
                label['relief'] = 'ridge'
                label.grid(column=1, row=row, sticky='new', padx=(1,0), pady=2)
 
             
 
 
if __name__ == '__main__':
    root = tk.Tk()
    controller = Controller(Database(), Window(root))
    root.mainloop()