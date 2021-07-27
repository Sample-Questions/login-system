import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import IntegrityError

class AccountManager:
    # Connect to the SQLite database
    def __init__(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect('example.db')
            self.cursor = self.connection.cursor()
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def initialize_tables(self):
        # clear data from previous executions
        # self.cursor.execute("drop table logins")

        self.cursor.execute('''create table logins
            (username text primary key, password_hash text);''')
        self.connection.commit()

    def create_account(self, username, password):
        password_hash = hash(password)
        try:
            self.cursor.execute("insert into logins values (?, ?);", (username, password_hash))
            self.connection.commit()
        except IntegrityError:
            return False
        return True

    def log_in(self, username, password):
        response = self.cursor.execute("select * from logins where username=?;", (username,)).fetchone()
        
        if response == None:
            return False

        password_hash = response[1]
        return str(hash(password)) == password_hash

    def close(self):
        self.connection.close()
