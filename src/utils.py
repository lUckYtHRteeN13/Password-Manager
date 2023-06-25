import os
import sqlite3

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
    
    @property
    def database_directory(self):
        return self._database_directory

    @database_directory.setter
    def database_directory(self, path):
        if not os.path.isdir(path):
            raise ValueError("Directory Path is Invalid")
        
        self._database_directory = path    

    def create_connection(self):
        pass

    def initialize_database(self):
        pass