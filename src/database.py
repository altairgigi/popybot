import sqlite3
import config

def initialise():
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            title TEXT,
            time TEXT,
            date TEXT
        )                    
    """)

    connection.commit()
    connection.close()

def add_memo(chat_id, title, time, date):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("INSERT INTO memo (chat_id, title, time, date) VALUES (?, ?, ?, ?)", (chat_id, title, time, date))

    connection.commit()
    connection.close()

def check_memo(time, date):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT id, chat_id, title FROM memo WHERE time = ? AND date = ?", (time, date))

    expired_memos = cursor.fetchall()

    if expired_memos:
        for memo in expired_memos:
            memo_id = memo[0]
            cursor.execute("DELETE FROM memo WHERE id = ?", (memo_id,))
    
    connection.commit()
    connection.close()

    return expired_memos

def get_memo_list(chat_id):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT title, time, date FROM memo WHERE chat_id = ?", (chat_id,))

    memo_list = cursor.fetchall()

    connection.commit()
    connection.close()

    return memo_list

def clean_memo_list(chat_id):
    connection = sqlite3.connect(config.DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM memo WHERE chat_id = ?", (chat_id,))

    connection.commit()
    connection.close()