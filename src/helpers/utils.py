from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from .config import get_settings
# 1. Define the Database URL

DATABASE_URL=get_settings.DATABASE_URL

if DATABASE_URL is None:
    raise ValueError("Not Found The DataBase URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close() 
        
        
