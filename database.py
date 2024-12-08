import sqlite3

conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    password TEXT,
    role INTEGER CHECK(role IN (0, 1)) NOT NULL -- 'admin', 'student'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    group_number INTEGER,
    FOREIGN KEY (student_id) REFERENCES Users(user_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    date DATE NOT NULL,
    status INTEGER CHECK(status IN (0, 1, 2)) NOT NULL,  -- 'Present', 'Absent', 'Late'
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS BonusPoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    points INTEGER NOT NULL,
    awarded_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_number INTEGER NOT NULL,
    project_title TEXT NOT NULL,
    project_source TEXT NOT NULL,
    submission_date DATE NOT NULL,
    FOREIGN KEY (group_number) REFERENCES Students(group_number)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS PeerReviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reviewer_id TEXT NOT NULL,
    reviewed_group_number INTEGER NOT NULL,
    feedback TEXT NOT NULL,
    score REAL CHECK(score BETWEEN 0 AND 10),
    review_date DATE NOT NULL,
    FOREIGN KEY (reviewer_id) REFERENCES Students(student_id)
)
''')

conn.commit()
conn.close()

