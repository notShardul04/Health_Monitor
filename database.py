from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Try to load from .env manually or rely on system env vars
# basic .env loading for simplicity if python-dotenv is not strictly required by prompt but good to have
# simpler approach: just read os.environ, assuming user/IDE loads it, or basic parsing
try:
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
except FileNotFoundError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:22Sh%40rdul@localhost:5432/health_monitor")

connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
