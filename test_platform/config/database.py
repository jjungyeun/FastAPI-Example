from test_platform import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# PostgreSQL URL
SQLALCHEMY_DATABASE_URL = settings.Rdb.scheme + settings.Rdb.id + ":" + settings.Rdb.pw + \
                          "@" + settings.Rdb.host + "/" + settings.Rdb.db_name


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