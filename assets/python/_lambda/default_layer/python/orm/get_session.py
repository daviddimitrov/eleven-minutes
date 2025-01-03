import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

def get_session():
    """
    Initialize database connection and return a SQLAlchemy session.
    """
    database_url = os.environ.get("DATABASE_URL", "mysql+pymysql://user:password@localhost/db")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Creates all tables based on models
    session = sessionmaker(bind=engine)
    return session()
