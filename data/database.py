from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from settings import settings

class Base(DeclarativeBase):
    pass

DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()