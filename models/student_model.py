import sqlite3

def connect_to_db():
    try:
        conn = sqlite3.connect("student_management.db")
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection error: {e}")

def get_student_by_id(student_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student
    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving student by ID: {e}")

def get_all_students():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        conn.close()
        return students
    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving all students: {e}")

def student_exists(student_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        raise RuntimeError(f"Error checking if student exists: {e}")

def create_student(student_id, full_name, cluster_number, group_number):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO Students (student_id, full_name, cluster_number, group_number) 
                       VALUES (?, ?, ?, ?)''', 
                       (student_id, full_name, cluster_number, group_number))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Integrity error: {e}")
    except sqlite3.Error as e:
        raise RuntimeError(f"Error creating student: {e}")

def update_student(student_id, full_name, cluster_number, group_number):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE Students SET full_name = ?, cluster_number = ?, group_number = ? 
                       WHERE student_id = ?''', 
                       (full_name, cluster_number, group_number, student_id))
        if cursor.rowcount == 0:
            raise ValueError("Student not found for update")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error updating student: {e}")

def delete_student(student_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Students WHERE student_id = ?', (student_id,))
        if cursor.rowcount == 0:
            raise ValueError("Student not found for deletion")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error deleting student: {e}")
