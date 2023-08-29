import sqlite3 as sq


class Database:
    '''
        Database class handles all the database functions.
        Create, insert, and retrieve
    '''
    def __init__(self):
        self.tables = ('rtbhigh', 'finisheshigh')
        #db_path = join(dirname(dirname(abspath(__file__))), 'data/highscores.db')
        self.connection = sq.connect("data/highscores.db")
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
 
