import datetime
import os

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Connection Settings
DB_USER = os.getenv("POSTGRES_USER", "anon")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "anon")
DB_NAME = os.getenv("POSTGRES_DB", "anon")
DB_HOST = os.getenv("POSTGRES_HOST", "anon")
DB_PORT = os.getenv("POSTGRES_PORT", 8080)

# SQLAlchemy Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define Message Table
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


# Initialize the Database (run once on startup)
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
