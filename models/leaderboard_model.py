import sqlite3

def connect_to_db():
    try:
        conn = sqlite3.connect('student_management.db')
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Error connecting to database: {str(e)}")

def get_leaderboard_scores():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Lấy điểm Attendance, Project và Volunteer cho tất cả sinh viên
        attendance_data = get_attendance_score(cursor)
        project_data = get_project_score(cursor)
        volunteer_data = get_volunteer_score(cursor)
        fullname_data = get_fullname(cursor)
        gpa_data = get_gpa(cursor)
        conn.close()

        result = []
        all_student_ids = set(attendance_data.keys()).union(project_data.keys()).union(volunteer_data.keys())

        for student in all_student_ids:
            attendance_score = attendance_data.get(student, 0)
            project_score = project_data.get(student, 0)
            volunteer_score = volunteer_data.get(student, 0)
            fullname = fullname_data.get(student, "Unknown")
            gpa = gpa_data.get(student, 0)
            
            if gpa is None:
                gpa = 0
            total_score = attendance_score + (0.5 * project_score) + volunteer_score + gpa

            result.append({
                "student_id": student,
                "full_name": fullname,
                "gpa": gpa,
                "attendance_score": attendance_score,
                "project_score": project_score,
                "volunteer_score": volunteer_score,
                "total_score": total_score
            })

        # Sắp xếp theo total_score giảm dần
        result.sort(key=lambda x: x['total_score'], reverse=True)

        # Gán rank cho từng sinh viên
        for index, student in enumerate(result):
            student["rank"] = index + 1
            
        return result

    except sqlite3.Error as e:
        raise RuntimeError(f"Error while fetching total scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

def get_attendance_score(cursor):
    try:
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

def get_project_score(cursor):
    try:
        cursor.execute("""
            SELECT student_id, 
                   IFNULL(project_score, 0) AS project_score
            FROM Students
        """)

        # Tính điểm cho từng sinh viên và trả về
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: project_score}

    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching project scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_project_score: {str(e)}")

def get_volunteer_score(cursor):
    try:
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

def get_fullname(cursor):
    try:
        cursor.execute("""
            SELECT student_id, 
                   full_name
            FROM Students
        """)

        # Tính điểm cho từng sinh viên và trả về
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: full_name}

    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching full names: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_fullname: {str(e)}")

def get_gpa(cursor):
    try:
        cursor.execute("""
            SELECT student_id, 
                   gpa
            FROM Students
        """)

        # Tính điểm cho từng sinh viên và trả về
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: gpa}

    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching GPAs: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_gpa: {str(e)}")