from superset import db
from superset.models.core import Database

sqlite_db = Database(database_name="SQLite-University", sqlalchemy_uri="sqlite:////app/university.db")
db.session.add(sqlite_db)
db.session.commit()