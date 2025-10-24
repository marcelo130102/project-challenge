from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from models import Base

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initializes database by creating all tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

