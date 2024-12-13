import sqlite3

# Kết nối với cơ sở dữ liệu
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Xóa view cũ nếu tồn tại
cursor.execute('DROP VIEW IF EXISTS Leaderboard')

# Tạo lại view với cột rank
cursor.execute('''
CREATE VIEW IF NOT EXISTS Leaderboard AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY 
        (
            COALESCE(a.attendance_score, 0) + 
            COALESCE(bp.volunteer_score, 0) + 
            COALESCE(s.project_score, 0) * 0.5 + 
            COALESCE(s.gpa, 0)
        ) DESC
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
    (
        COALESCE(a.attendance_score, 0) + 
        COALESCE(bp.volunteer_score, 0) + 
        COALESCE(s.project_score, 0) * 0.5 + 
        COALESCE(s.gpa, 0)
    ) AS total_score
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
ORDER BY total_score DESC;
''')

# Xác nhận thay đổi
conn.commit()
conn.close()
