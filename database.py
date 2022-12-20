from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Setting
settings = {
    "scheme": "postgresql://",
    "id": "testuser",
    "pw": "testuser!",
    "host": "localhost:5432",
    "db_name": "testdb"
}
SQLALCHEMY_DATABASE_URL = settings["scheme"] + settings["id"] + ":" + settings["pw"] + \
                          "@" + settings["host"] + "/" + settings["db_name"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()