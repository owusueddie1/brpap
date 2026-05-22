import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use Supabase PostgreSQL connection string from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:YOUR-PASSWORD@db.abqtiwmbkolcjabinwip.supabase.co:5432/postgres"
)

# For PostgreSQL, we don't need the check_same_thread argument
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
