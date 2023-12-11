import sqlite3
from sqlite3 import Error
import glob
import config
class Migrate:

    def __init__(self, db, path):
        self.db = db
        self.path = path

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def migrate(self):
        con = self.create_connection()
        if con:
            files = glob.glob(self.path)
            
            for f in files:
                cur = con.cursor() 
                with open(f, "r") as f_in:
                    sql = f_in.read() 
                cur.executescript(sql)
            
            con.close()

if __name__ == '__main__':
    mg = Migrate(config.db, config.db_migrate)
    mg.migrate()