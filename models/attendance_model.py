import sqlite3
from datetime import datetime

def connect_to_db():
    try:
        conn = sqlite3.connect("student_management.db")
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection error: {e}")

def get_all_attendance(student_id=None):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        if student_id:
            cursor.execute("SELECT * FROM Attendance WHERE student_id = ?", (student_id,))
        else:
            cursor.execute("SELECT * FROM Attendance")

        records = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "student_id": row[1], "date": row[2], "status": row[3]} for row in records]
    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving attendance: {e}")

def get_attendance_by_id(id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Attendance WHERE id = ?", (id,))
        record = cursor.fetchone()
        conn.close()

        if record:
            return {"id": record[0], "student_id": record[1], "date": record[2], "status": record[3]}
        return None
    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving attendance by ID: {e}")

def create_attendance_record(data):
    try:
        date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Attendance (student_id, date, status) VALUES (?, ?, ?)",
            (data["student_id"], date, data["status"]),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise ValueError(f"Attendance record for student {data['student_id']} on {data['date']} already exists.")
        else:
            raise ValueError(f"Integrity error: {e}")
    except sqlite3.Error as e:
        raise RuntimeError(f"Error creating attendance record: {e}")

def update_attendance_record(id, data):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Attendance SET status = ? WHERE id = ?",
            (data["status"], id),
        )
        if cursor.rowcount == 0:
            raise ValueError("Attendance record not found for update")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error updating attendance record: {e}")

def delete_attendance_record(id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Attendance WHERE id = ?", (id,))
        if cursor.rowcount == 0:
            raise ValueError("Attendance record not found for deletion")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error deleting attendance record: {e}")
