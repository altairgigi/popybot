import sqlite3
import config

def initialise():
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    #create table for memos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            title TEXT,
            time TEXT,
            date TEXT
        )                    
    """)

    #create table for routines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            title TEXT,
            time TEXT
        )
    """)

    #create table for user settings, mainly for the daily digest
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            chat_id INTEGER PRIMARY KEY,
            digest_time TEXT NOT NULL,
            location TEXT NOT NULL
        )                    
    """)

    connection.commit()
    connection.close()

def add_memo(chat_id, title, time, date):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("INSERT INTO memo (chat_id, title, time, date) "
                   "VALUES (?, ?, ?, ?)", (chat_id, title, time, date))

    connection.commit()
    connection.close()

def delete_memo(chat_id, number):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM memo "
                   "WHERE id = ("
                   "SELECT id "
                   "FROM ( "
                   "SELECT id, ROW_NUMBER() OVER (ORDER BY date, time) AS n "
                   "FROM memo "
                   "WHERE chat_id = ?) "
                   "WHERE n = ?)", (chat_id, number))

    connection.commit()
    connection.close()

def check_memo(time, date):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT id, chat_id, title "
                   "FROM memo "
                   "WHERE time = ? AND date = ?", (time, date))

    expired_memos = cursor.fetchall()

    if expired_memos:
        for memo in expired_memos:
            memo_id = memo[0]
            cursor.execute("DELETE FROM memo "
                           "WHERE id = ?", (memo_id,))
    
    connection.commit()
    connection.close()

    return expired_memos

def clean_memo_list(chat_id):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM memo "
                   "WHERE chat_id = ?", (chat_id,))

    connection.commit()
    connection.close()

def get_memo_list(chat_id):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT title, time, date "
                   "FROM memo "
                   "WHERE chat_id = ? "
                   "ORDER BY date, time", (chat_id,))

    memo_list = cursor.fetchall()

    connection.commit()
    connection.close()

    return memo_list

def get_daily_memo_list(chat_id, date):
    connection = sqlite3.connect(config.DATABASE_NAME)
    
    cursor = connection.cursor()

    cursor.execute("SELECT title, time " 
                   "FROM memo " 
                   "WHERE chat_id = ? and date = ? "
                   "UNION ALL "
                   "SELECT title, time " 
                   "FROM routines " 
                   "WHERE chat_id = ? "     
                   "ORDER BY time", (chat_id, date, chat_id,))

    daily_memo_list = cursor.fetchall()

    connection.commit()
    connection.close()

    return daily_memo_list

def get_digest_list(time):
    connection = sqlite3.connect(config.DATABASE_NAME)
    
    cursor = connection.cursor()

    cursor.execute("SELECT chat_id, location "
                   "FROM user_settings "
                   "WHERE digest_time = ?", (time,))

    digest_list = cursor.fetchall()

    connection.commit()
    connection.close()

    return digest_list

def add_routine(chat_id, title, time):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("INSERT INTO routines (chat_id, title, time) "
                   "VALUES (?, ?, ?)", (chat_id, title, time))

    connection.commit()
    connection.close()

def delete_routine(chat_id, number):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM routines "
                   "WHERE id = ("
                   "SELECT id "
                   "FROM ( "
                   "SELECT id, ROW_NUMBER() OVER (ORDER BY time) AS n "
                   "FROM routines "
                   "WHERE chat_id = ?) "
                   "WHERE n = ?)", (chat_id, number))

    connection.commit()
    connection.close()

def clean_routines(chat_id):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM routines "
                   "WHERE chat_id = ?", (chat_id,))

    connection.commit()
    connection.close()

def get_routines(time):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT chat_id, title "
                   "FROM routines "
                   "WHERE time = ?", (time,))

    routines = cursor.fetchall()

    connection.commit()
    connection.close()

    return routines

def get_routine_list(chat_id):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT title, time "
                   "FROM routines "
                   "WHERE chat_id = ? "
                   "ORDER BY time", (chat_id,))

    routine_list = cursor.fetchall()

    connection.commit()
    connection.close()

    return routine_list

def set_user_settings(chat_id, digest_time, location):
    connection = sqlite3.connect(config.DATABASE_NAME)
    
    cursor = connection.cursor()

    cursor.execute("INSERT OR REPLACE INTO user_settings (chat_id, digest_time, location) "
                   "VALUES (?, ?, ?)", (chat_id, digest_time, location))

    connection.commit()
    connection.close()