import sqlite3

# Kết nối đến SQLite database
conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM Students")
rows = cursor.fetchall()

# cursor.execute("SELECT * FROM Users")
# rows = cursor.fetchall()

# cursor.execute("SELECT * FROM Attendance")
# rows = cursor.fetchall()

# cursor.execute("SELECT * FROM BonusPoints")
# rows = cursor.fetchall()

# In kết quả
for row in rows:
    print(row)

# cursor.execute("DELETE FROM Users where user_id = '2151163668'")
# conn.commit()

# Đóng kết nối
conn.close()