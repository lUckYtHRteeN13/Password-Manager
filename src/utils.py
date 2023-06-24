import os

APP_PATH = os.path.abspath(os.getcwd())import os
import sqlite3

APP_PATH = os.path.abspath(os.getcwd())
def generate_db_file():
    if not os.path.exists(DATABASE_DIRECTORY):
        os.makedirs(DATABASE_DIRECTORY)

    database = os.path.join(DATABASE_DIRECTORY, "app.db")

    return database

def create_connection():
    pass

def initialize_database():
    pass

if __name__ == "__main__":
    generate_db_file()