import os, sqlite3, re

USER_DIRECTORY = os.path.expanduser("~\AppData\Local")
DATA_DIRECTORY = os.path.join(USER_DIRECTORY, "Password Manager")


def show_password(button, widget):
    def inner():
        if button["relief"] == "raised":
            button.config(relief="sunken")
            widget.config(show="")
        else:
            button.config(relief="raised")
            widget.config(show="•")
        return inner
    button['command'] = inner

# DATABASE Handling
class DatabaseHandler:
    def __init__(self):
        self._database_directory = os.path.join(DATA_DIRECTORY, "database")
        
        if not os.path.exists(self.database_directory):
            os.makedirs(self.database_directory)

        self._file_name = "main.db"
        self._file_path = os.path.join(self.database_directory, self.file_name)
        self.initialize_database()
    
    @property
    def database_directory(self) -> str:
        return self._database_directory

    @database_directory.setter
    def database_directory(self, path:str):
        if not os.path.isdir(path):
            raise ValueError("Directory Path is Invalid")
        
        self._database_directory = path    

    @property
    def file_name(self) -> str:
        return self._file_name
    
    @file_name.setter
    def file_name(self, name:str):
        if not re.search(".db$", name):
            raise ValueError(f"Invalid file extension")
        
        self._file_name = name
        self._file_path = os.path.join(self.database_directory, self.file_name)

    @property
    def file_path(self) -> str:
        return self._file_path
    
    @file_path.setter
    def file_path(self, path:str):
        if not os.path.isdir(path):
            raise ValueError("Directory Path is Invalid")
        
        self._file_path = path

    def connect(func):
        def inner(self, table_name=None, *headers, **data):

            with sqlite3.connect(self.file_path) as conn:
                if not table_name:
                    return func(self, conn)
                elif data:
                    return func(self, conn, table_name, **data)
                else:
                    return func(self, conn, table_name, *headers)
                
        return inner

    @connect
    def add_data(self, conn, table_name, **data):
        #TODO: Find  out how to not duplicate this data
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table_name} {tuple(data.keys())} VALUES {tuple(data.values())}")

    @connect
    def initialize_database(self, conn):
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Applications (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Accounts (ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, application INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (ID), FOREIGN KEY (application) REFERENCES Applications (ID))""")

    @connect
    def get_info(self, conn, table_name, columns="*", **data):
        cur = conn.cursor()

        if isinstance(columns, tuple):
            columns = ', '.join(str(item) for item in columns)

        command = f"SELECT {columns} FROM {table_name} WHERE {', '.join(data.keys())} IN ({', '.join(['?']*len(data))})"
        cur.execute(command, tuple(data.values()))
        results = cur.fetchone()
        return results