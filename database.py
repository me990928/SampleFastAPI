""" 同期通信でデータベースとの接続を行うためのモジュール """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
        }
    )

Sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """ Function to get a database session 
        Returns:
        Sessionmaker: A SQLAlchemy session to interact with the database
    """
    db = Sessionmaker()
    try:
        yield db
    finally:
        db.close()
