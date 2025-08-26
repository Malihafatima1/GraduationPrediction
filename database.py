import sqlite3

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            email TEXT, 
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            username TEXT, 
            inputs TEXT, 
            svm_result TEXT, 
            rf_result TEXT
        )
    ''')
    conn.commit()

def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def insert_user(username, email, password):
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, password))
    conn.commit()

def validate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

def update_password(username, new_password):
    c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    conn.commit()

def save_prediction(username, inputs, svm_result, rf_result):
    c.execute("INSERT INTO predictions VALUES (?, ?, ?, ?)", (username, str(inputs), svm_result, rf_result))
    conn.commit()

def get_predictions(username=None):
    if username:
        return c.execute("SELECT * FROM predictions WHERE username=?", (username,)).fetchall()
    else:
        return c.execute("SELECT * FROM predictions").fetchall()

def get_all_users():
    return c.execute("SELECT username, email FROM users").fetchall()
