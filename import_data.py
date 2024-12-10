import sqlite3
import requests
import bcrypt
from datetime import datetime, timedelta

spreadsheet_id = '1jSTFR5O8Vi1LYp-w02jFH_eqZtlc7W8-X5j8_H0D90k' 
range_ = 'DS_DiemDanh_15cot!A1:X68' 
api_key = 'AIzaSyDMaZNpl9Kg-MkBfjhpTFE0XdsPaQQsIKs' 

url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}?key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()['values'] 
else:
    print(f"Error: {response.status_code}")
    exit()

spreadsheet_id = '1gkEoNyGar6bqgAQRJdFlpvIK033j821K1pk5vUWJyss' 
range_ = 'Trang tính1!A1:C66' 
api_key = 'AIzaSyDMaZNpl9Kg-MkBfjhpTFE0XdsPaQQsIKs' 

url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}?key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data2 = response.json()['values'] 
else:
    print(f"Error: {response.status_code}")
    exit()

password = "admin"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()

cursor.execute("""
INSERT OR REPLACE INTO Users (user_id, role, password)
VALUES (?, ?, ?)
""", ('admin', 0, hashed_password))

for row in data[9:68]:  
    student_id = row[1]
    full_name = row[2] + " " + row[3]
    cursor.execute("""
    INSERT INTO Users (user_id, role)
    VALUES (?, ?)
    """, (student_id, 1))

for row in data[9:68]:  
    student_id = row[1]
    full_name = row[2] + " " + row[3]  
    class_name = row[4]
    cursor.execute("""
    INSERT INTO Students (student_id, full_name, class_name)
    VALUES (?, ?, ?)
    """, (student_id, full_name, class_name))

attendance_dates = data[8][5:]

for row in data[9:68]:
    student_id = row[1]
    attendance_data = row[5:21] 

    for i, status in enumerate(attendance_data):  
        if i >= len(attendance_dates):
            break

        current_date = attendance_dates[i]  

        if current_date:
            status_code = None
            if status == 'pb' or status == '':  
                status_code = 1
            elif status == 'v':  
                status_code = 0

            if status_code is not None:
                cursor.execute("""
                INSERT INTO Attendance (student_id, date, status)
                VALUES (?, ?, ?)
                """, (student_id, current_date, status_code))

            if status == 'pb':
                cursor.execute("""
                INSERT INTO BonusPoints (student_id, points, awarded_date)
                VALUES (?, ?, ?)
                """, (student_id, 1, current_date))

cluster_number = 1
i = j = 0
for row in data2:
    if i == 22:
        cluster_number += 1
        i = 0
    if i == 2 or i == 7 or i == 12 or i == 17:
        group_number = row[0]
        project_title = row[2]
    if i > 1 and j != 38:
        full_name = row[1]

        cursor.execute('''
        UPDATE Students 
        SET cluster_number = ?, group_number = ?
        WHERE full_name = ?
        ''', (cluster_number, group_number, full_name))

        cursor.execute('''
        INSERT INTO Projects (student_id, project_title)
        SELECT student_id, ?
        FROM Students
        WHERE full_name = ?
        ''', (project_title, full_name))

    i+=1
    j+=1
    
# Commit và đóng kết nối
conn.commit()
conn.close()
