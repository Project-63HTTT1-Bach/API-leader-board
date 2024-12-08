import sqlite3
from openpyxl import load_workbook
import os
import bcrypt

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

# cursor.execute("""
# INSERT OR REPLACE INTO Users (user_id, full_name, role, password)
# VALUES (?, ?, ?, ?)
# """, ('admin', 'admin', 0, hashed_password))

# for row in data:
#     cursor.execute("""
#     INSERT INTO Users (user_id, full_name, role)
#     VALUES (?, ?, ?)
#     """, (row[1], row[2] + " " + row[3], 1))

conn.commit()
conn.close()