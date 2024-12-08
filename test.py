import sqlite3

# Kết nối đến SQLite database
conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()

# cursor.execute("DELETE FROM students")
# conn.commit()

# cursor.execute("SELECT * FROM Users")
# rows = cursor.fetchall()

cursor.execute("SELECT * FROM Attendance")
rows = cursor.fetchall()

# cursor.execute("SELECT * FROM BonusPoints")
# rows = cursor.fetchall()

# In kết quả
for row in rows:
    print(row)

# Đóng kết nối
conn.close()