import sqlite3

conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    class_name TEXT NOT NULL,
    cluster_number INTEGER,
    group_number INTEGER,
    project_score INTEGER,
    gpa REAL,
    FOREIGN KEY (student_id) REFERENCES Users(user_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    date DATE NOT NULL,
    status INTEGER CHECK(status IN (0, 1)) NOT NULL,  -- 'Absent', 'Present'
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    CONSTRAINT unique_attendance UNIQUE (student_id, date)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS BonusPoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    points INTEGER NOT NULL,
    awarded_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    project_title TEXT NOT NULL,
    project_source TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
)
''')

conn.commit()
conn.close()

