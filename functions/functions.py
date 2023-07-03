import os
import sqlite3
from datetime import date

def get_database_connection():
    '''
        Creates a connection between selected database
    '''
    
    sqlite_file = 'rewards.db'
    file_exists = os.path.isfile(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    if not file_exists:
        create_sqlite_tables(conn)
    return conn

def create_sqlite_tables(conn):
    '''
        Creates a sqlite table as specified in schema_sqlite.sql file
    '''
    cursor = conn.cursor()
    with open('sqlite_schema.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()

def insert_search_count(email, count):
    '''
        Inserts a new user into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (email, search_count) VALUES (?, ?)", (email, count))
        conn.commit()
        cursor.close()
    except:
        cursor.close()

def update_search_count(email, count):
    '''
        Inserts a new user into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE logs set search_count=? WHERE email=?", (count, email))
        conn.commit()
        cursor.close()
    except:
        cursor.close()

def get_search_count_by_email(email):
    '''
        Returns total number of searches done by all profiles
    '''
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs WHERE email=? and run_date=?', (email, date.today()))
    results = cursor.fetchone()
    return results