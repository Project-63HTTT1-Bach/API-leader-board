from superset import db
from superset.models.core import Database

sqlite_db = Database(database_name="student_management", sqlalchemy_uri="sqlite:////app/student_management.db")
db.session.add(sqlite_db)
db.session.commit()