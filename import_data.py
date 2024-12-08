import sqlite3
from openpyxl import load_workbook
import os
import bcrypt
from datetime import datetime, timedelta

excel_file = "Danh sách điểm danh HTKDTM 63HTTT1.xlsx"

if not os.path.exists(excel_file):
    print(f"File '{excel_file}' không tồn tại.")
else:
    print(f"File '{excel_file}' tồn tại.")

password = "admin"  
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()

workbook = load_workbook(filename=excel_file, data_only=True)
sheet = workbook.active

rows = list(sheet.iter_rows(values_only=True))
data = rows[9:68]   
# print(data)

cursor.execute("""
INSERT OR REPLACE INTO Users (user_id, full_name, role, password)
VALUES (?, ?, ?, ?)
""", ('admin', 'admin', 0, hashed_password))

for row in data:
    cursor.execute("""
    INSERT INTO Users (user_id, full_name, role)
    VALUES (?, ?, ?)
    """, (row[1], row[2] + " " + row[3], 1))

for row in data:
    cursor.execute("""
    INSERT INTO Students (student_id, full_name)
    VALUES (?, ?)
    """, (row[1], row[2] + " " + row[3]))

for row in data:
    student_id = row[1]
    attendance_data = row[5:21]
    start_date = datetime(2024, 11, 12)  # Ngày bắt đầu từ 12/11/2024 (thứ 3)
    end_date = datetime(2024, 12, 6)  # Giới hạn ngày cuối là 06/12/2024
    
    for i, status in enumerate(attendance_data):
        current_date = start_date + timedelta(weeks=i//2, days=(i % 2) * 3)
        
        if current_date > end_date:
            break
        
        status_code = 1 if status == 'pb' or status is None else 0 if status == 'v' else None
        
        if status_code is not None:  
            cursor.execute("""
            INSERT INTO Attendance (student_id, date, status)
            VALUES (?, ?, ?)
            """, (student_id, current_date.date(), status_code))

        if status == 'pb':
            cursor.execute("""
            INSERT INTO BonusPoints (student_id, reason, points, awarded_date)
            VALUES (?, ?, ?, ?)
            """, (student_id, "Participation in class", 1, current_date.date())) 

conn.commit()
conn.close()