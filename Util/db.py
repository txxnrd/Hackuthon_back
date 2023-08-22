import sqlite3

class DB:
    
    def __init__(self, DB_name):
        self.name = DB_name
        self.conn = None
        self.cur = None
        
    def connect(self):
        self.conn = sqlite3.connect(self.name)
        self.cur = self.conn.cursor()
        return
    
    def commit(self):
        self.conn.commit()
    
    def execute(self, command:str, get_result=True, is_commit=True):
        try:
            self.cur.execute(command)
        except:
            self.connect()
            self.cur.execute(command)
        
        if is_commit:
            self.commit()
        if get_result:        
            return self.cur.fetchall()
        return
    
    def close(self):
        self.conn.close()

currentDB = DB('app/database/now.db')