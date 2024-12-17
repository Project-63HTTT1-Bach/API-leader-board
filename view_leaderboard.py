import sqlite3

# Hàm kết nối cơ sở dữ liệu
def connect_to_db():
    try:
        conn = sqlite3.connect('student_management.db')
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Error connecting to database: {str(e)}")

# Hàm tạo view Leaderboard với CTE
def create_leaderboard_view():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Xóa view cũ nếu tồn tại
        cursor.execute('DROP VIEW IF EXISTS Leaderboard')

        # Tạo view Leaderboard sử dụng CTE
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS Leaderboard AS
            WITH ScoreRange AS (
                SELECT 
                    MAX(
                        COALESCE(a.attendance_score, 0) + 
                        COALESCE(bp.volunteer_score, 0) + 
                        COALESCE(s.project_score, 0) * 0.5
                    ) AS max_score,
                    MIN(
                        COALESCE(a.attendance_score, 0) + 
                        COALESCE(bp.volunteer_score, 0) + 
                        COALESCE(s.project_score, 0) * 0.5
                    ) AS min_score
                FROM Students s
                LEFT JOIN (
                    SELECT 
                        student_id, 
                        SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS attendance_score
                    FROM Attendance
                    GROUP BY student_id
                ) a ON s.student_id = a.student_id
                LEFT JOIN (
                    SELECT 
                        student_id, 
                        SUM(points) AS volunteer_score
                    FROM BonusPoints
                    GROUP BY student_id
                ) bp ON s.student_id = bp.student_id
            )
            SELECT 
                ROW_NUMBER() OVER (
                    ORDER BY normalized_score DESC, COALESCE(s.gpa, 0) DESC
                ) AS rank,
                s.student_id,
                s.full_name,
                s.class_name,
                s.cluster_number,
                s.group_number,
                COALESCE(s.gpa, 0) AS gpa,
                COALESCE(a.attendance_score, 0) AS attendance_score,
                COALESCE(bp.volunteer_score, 0) AS volunteer_score,
                COALESCE(s.project_score, 0) AS project_score,
                ROUND(10.0 * (
                    (COALESCE(a.attendance_score, 0) + 
                     COALESCE(bp.volunteer_score, 0) + 
                     COALESCE(s.project_score, 0) * 0.5
                    ) - sr.min_score
                ) / (sr.max_score - sr.min_score), 2) AS normalized_score,
                ROUND(10.0 * (
                    (COALESCE(a.attendance_score, 0) + 
                     COALESCE(bp.volunteer_score, 0) + 
                     COALESCE(s.project_score, 0) * 0.5
                    ) - sr.min_score
                ) / (sr.max_score - sr.min_score), 2) AS total_score
            FROM Students s
            LEFT JOIN (
                SELECT 
                    student_id, 
                    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS attendance_score
                FROM Attendance
                GROUP BY student_id
            ) a ON s.student_id = a.student_id
            LEFT JOIN (
                SELECT 
                    student_id, 
                    SUM(points) AS volunteer_score
                FROM BonusPoints
                GROUP BY student_id
            ) bp ON s.student_id = bp.student_id
            JOIN ScoreRange sr
            ORDER BY normalized_score DESC, COALESCE(s.gpa, 0) DESC;
        ''')

        # Xác nhận thay đổi
        conn.commit()
        print("View 'Leaderboard' đã được tạo thành công.")

    except sqlite3.Error as e:
        print(f"SQLite Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
    finally:
        if conn:
            conn.close()

# Chạy hàm tạo view
if __name__ == "__main__":
    create_leaderboard_view()
