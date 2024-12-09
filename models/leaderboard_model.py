import sqlite3

def connect_to_db():
    try:
        conn = sqlite3.connect('student_management.db')
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Error connecting to database: {str(e)}")

def get_leaderboard_scores(student_id=None):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Lấy điểm Attendance, Project và Volunteer
        attendance_data = get_attendance_score(cursor, student_id)
        project_data = get_project_score(cursor, student_id)
        volunteer_data = get_volunteer_score(cursor, student_id)

        conn.close()

        result = []
        all_student_ids = set(attendance_data.keys()).union(project_data.keys()).union(volunteer_data.keys())

        for student in all_student_ids:
            attendance_score = attendance_data.get(student, 0)
            project_score = project_data.get(student, 0)
            volunteer_score = volunteer_data.get(student, 0)
            
            total_score = attendance_score + (0.5 * project_score) + volunteer_score

            result.append({
                "student_id": student,
                "attendance_score": attendance_score,
                "project_score": project_score,
                "volunteer_score": volunteer_score,
                "total_score": total_score
            })

        return result

    except sqlite3.Error as e:
        raise RuntimeError(f"Error while fetching total scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

def get_attendance_score(cursor, student_id=None):
    try:
        if student_id:
            cursor.execute("""
                SELECT student_id, 
                        SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS attendance_score
                FROM Attendance
                WHERE student_id = ?
                GROUP BY student_id
            """, (student_id,))
        else:
            cursor.execute("""
                SELECT student_id, 
                        SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS attendance_score
                FROM Attendance
                GROUP BY student_id
            """)

        # Tính điểm cho từng sinh viên và trả về
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: attendance_score}
    
    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching attendance scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_attendance_score: {str(e)}")

def get_project_score(cursor, student_id=None):
    try:
        if student_id:
            cursor.execute("""
                SELECT s.student_id, 
                       IFNULL(SUM(p.project_score), 0) AS project_score
                FROM Projects p
                JOIN Students s ON s.group_number = p.group_number  -- Liên kết với Students bằng group_number
                WHERE s.student_id = ?  -- Điều kiện để lấy điểm cho sinh viên cụ thể
                GROUP BY s.student_id
            """, (student_id,))
        else:
            cursor.execute("""
                SELECT s.student_id, 
                       IFNULL(SUM(p.project_score), 0) AS project_score
                FROM Projects p
                JOIN Students s ON s.group_number = p.group_number  -- Liên kết với Students bằng group_number
                GROUP BY s.student_id
            """)

        # Tính điểm cho từng sinh viên và trả về
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: project_score}

    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching project scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_project_score: {str(e)}")

def get_volunteer_score(cursor, student_id=None):
    try:
        if student_id:
            cursor.execute("""
                SELECT student_id, 
                        IFNULL(SUM(points), 0) AS volunteer_score
                FROM BonusPoints
                WHERE student_id = ?
                GROUP BY student_id
            """, (student_id,))
        else:
            cursor.execute("""
                SELECT student_id, 
                        IFNULL(SUM(points), 0) AS volunteer_score
                FROM BonusPoints
                GROUP BY student_id
            """)

        # Tính điểm cho từng sinh viên và trả về
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: volunteer_score}

    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching volunteer scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_volunteer_score: {str(e)}")
