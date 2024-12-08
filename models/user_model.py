import sqlite3
import bcrypt

def get_user_from_db(username):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password, role FROM Users WHERE user_id = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "user_id": user[0],
            "password": user[1],
            "role": user[2]
        }
    return None

def create_user(user_id):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO Users (user_id, role) 
                   VALUES (?, ?)''', 
                   (user_id, 1))
    conn.commit()
    conn.close()

def check_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password)