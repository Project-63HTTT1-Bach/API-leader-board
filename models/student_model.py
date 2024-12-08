import sqlite3

def get_student_by_id(student_id):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student

def get_all_students():
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()
    return students

def student_exists(student_id):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Students WHERE student_id = ?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def full_name_exists_except_id(student_id, full_name):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Students WHERE full_name = ? AND student_id != ?", (full_name, student_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def create_student(student_id, full_name, group_number):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO Students (student_id, full_name, group_number) 
                   VALUES (?, ?, ?)''', 
                   (student_id, full_name, group_number))
    conn.commit()
    conn.close()

def update_student(student_id, full_name, group_number):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''UPDATE Students SET full_name = ?, group_number = ? WHERE student_id = ?''', 
                   (full_name, group_number, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM Students WHERE student_id = ?''', (student_id,))
    conn.commit()
    conn.close()
