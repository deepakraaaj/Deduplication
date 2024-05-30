import sqlite3

def get_db_connection():
    conn = sqlite3.connect('data/index.db', check_same_thread=False)
    return conn

def initialize_db(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS subset (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        file CHAR(200),
        master CHAR(200),
        rate INTEGER, start INTEGER, end INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS master (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        file CHAR(200),
        s3_key CHAR(200),
        format TEXT,
        rate INTEGER, dimension INTEGER, length INTEGER)''')

    cursor.connection.commit()

def insert_user(cursor, username, password):
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    cursor.connection.commit()

def get_user_by_credentials(cursor, username, password):
    return cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()

def get_user_by_id(cursor, user_id):
    return cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def insert_master_file(cursor, user, filename, s3_key, data_format, rate, dimension, length):
    cursor.execute('INSERT INTO master (user, file, s3_key, format, rate, dimension, length) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                   (user, filename, s3_key, data_format, rate, dimension, length))
    cursor.connection.commit()

def insert_subset(cursor, user, filename, master, rate, start, end):
    cursor.execute('INSERT INTO subset (user, file, master, rate, start, end) VALUES (?, ?, ?, ?, ?, ?)', 
                   (user, filename, master, rate, start, end))
    cursor.connection.commit()

def get_all_subsets(cursor):
    return cursor.execute('SELECT * FROM subset').fetchall()

def get_all_master_files(cursor, data_format, dimension, length):
    query = "SELECT s3_key FROM master WHERE format = ? AND dimension = ? AND length >= ?"
    return cursor.execute(query, (data_format, dimension, length)).fetchall()
