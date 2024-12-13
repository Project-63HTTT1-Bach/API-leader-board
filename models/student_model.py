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

        cursor.execute("""
            SELECT 
                s.student_id,
                s.full_name, 
                s.class_name, 
                s.cluster_number, 
                s.group_number, 
                s.project_score,
                s.gpa, 
                IFNULL(a.attendance_score, 0) AS attendance_score, 
                IFNULL(bp.volunteer_score, 0) AS volunteer_score
            FROM Students s
            LEFT JOIN (
                SELECT student_id, SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS attendance_score
                FROM Attendance
                GROUP BY student_id
            ) a ON s.student_id = a.student_id
            LEFT JOIN (
                SELECT student_id, SUM(points) AS volunteer_score
                FROM BonusPoints
                GROUP BY student_id
            ) bp ON s.student_id = bp.student_id
            WHERE s.student_id = ?
        """, (student_id,))

        student = cursor.fetchone()
        conn.close()
        
        if student:
            return {
                "student_id": student[0],
                "full_name": student[1],
                "class_name": student[2],
                "cluster_number": student[3],
                "group_number": student[4],
                "project_score": student[5],
                "gpa": student[6],
                "attendance_score": student[7],
                "volunteer_score": student[8]            }
        else:
            return None

    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving student by ID: {e}")

def update_gpa(student_id, gpa):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Students
            SET gpa = ?
            WHERE student_id = ?
        """, (gpa, student_id))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error updating GPA: {e}")