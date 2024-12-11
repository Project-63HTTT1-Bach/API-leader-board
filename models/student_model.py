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

        # Truy vấn thông tin từ bảng Students
        cursor.execute("""
            SELECT 
                s.full_name, 
                s.class_name, 
                s.cluster_number, 
                s.group_number, 
                s.project_score, 
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
                "full_name": student[0],
                "class_name": student[1],
                "cluster_number": student[2],
                "group_number": student[3],
                "project_score": student[4],
                "attendance_score": student[5],
                "volunteer_score": student[6]
            }
        else:
            return None

    except sqlite3.Error as e:
        raise RuntimeError(f"Error retrieving student by ID: {e}")
