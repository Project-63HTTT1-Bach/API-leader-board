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

        # Lấy dữ liệu cần thiết từ database
        attendance_data = get_total_absent_days(cursor)  # Tổng số buổi vắng
        volunteer_data = get_volunteer_score(cursor)    # Điểm phát biểu
        fullname_data = get_fullname(cursor)            # Họ và tên
        gpa_data = get_gpa(cursor)                      # GPA
        conn.close()

        result = []
        all_student_ids = set(attendance_data.keys()).union(volunteer_data.keys())

        for student in all_student_ids:
            total_absent_days = attendance_data.get(student, 0)
            volunteer_score = volunteer_data.get(student, 0)
            fullname = fullname_data.get(student, "Unknown")
            gpa = gpa_data.get(student, 0)

            # Tính điểm Attendance (mặc định 5 điểm, mỗi buổi vắng -0.5)
            attendance_score = max(0, 5 - (0.5 * total_absent_days))

            # Điểm phát biểu (+0.5 mỗi điểm)
            adjusted_volunteer_score = volunteer_score * 0.5

            # Tổng điểm mới
            total_score = attendance_score + adjusted_volunteer_score

            result.append({
                "student_id": student,
                "full_name": fullname,
                "gpa": gpa if gpa is not None else 0,
                "attendance_score": attendance_score,
                "volunteer_score": adjusted_volunteer_score,
                "total_score": total_score
            })

        # Sắp xếp theo total_score giảm dần, nếu bằng nhau thì xét gpa giảm dần
        result.sort(key=lambda x: (-x['total_score'], -x['gpa']))

        # Gán rank cho từng sinh viên
        for index, student in enumerate(result):
            student["rank"] = index + 1

        return result

    except sqlite3.Error as e:
        raise RuntimeError(f"Error while fetching total scores: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

# def get_attendance_score(cursor):
#     try:
#         cursor.execute("""
#             SELECT student_id, 
#                    SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS attendance_score
#             FROM Attendance
#             GROUP BY student_id
#         """)

#         # Tính điểm cho từng sinh viên và trả về
#         records = cursor.fetchall()
#         return {row[0]: row[1] for row in records}  # Trả về một dict {student_id: attendance_score}
    
#     except sqlite3.Error as e:
#         raise RuntimeError(f"Error fetching attendance scores: {str(e)}")
#     except Exception as e:
#         raise RuntimeError(f"An unexpected error occurred in get_attendance_score: {str(e)}")

def get_total_absent_days(cursor):
    """ Trả về tổng số buổi vắng của từng sinh viên. """
    try:
        cursor.execute("""
            SELECT student_id, 
                   SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS total_absent_days
            FROM Attendance
            GROUP BY student_id
        """)
        records = cursor.fetchall()
        return {row[0]: row[1] for row in records}  # {student_id: total_absent_days}

    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching total absent days: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred in get_total_absent_days: {str(e)}")

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
