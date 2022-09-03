from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import SQLALCHEMY_CONNECTION_URI

# Create database engine
engine = create_engine(SQLALCHEMY_CONNECTION_URI, connect_args={"check_same_thread": False})

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base for declaring db classes (tables)
Base = declarative_base()

# Enable foreign key support in sqlite
if engine.url.drivername == "sqlite":
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
