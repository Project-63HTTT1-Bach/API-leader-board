import sqlite3
import bcrypt

def connect_to_db():
    try:
        conn = sqlite3.connect("student_management.db")
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection error: {e}")

def get_user_from_db(username):
    try:
        conn = connect_to_db()
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
    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving user from database: {e}")

def create_user(user_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        password = user_id + ""  
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO Users (user_id, password, role) 
            VALUES (?, ?, ?)''', 
            (user_id, hashed_password, 1))  
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Integrity error: {e}")
    except sqlite3.Error as e:
        raise RuntimeError(f"Error creating user: {e}")

def delete_user(user_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
        if cursor.rowcount == 0:
            raise ValueError("User not found for deletion")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error deleting student: {e}")

def check_password(input_password, stored_password):
    try:
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_password)
    except Exception as e:
        raise RuntimeError(f"Error checking password: {e}")
