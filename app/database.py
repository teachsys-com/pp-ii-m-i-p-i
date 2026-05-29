import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection string from environment or default
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/questions_db")

# # Fallback to SQLite if postgresql engine creation fails or if we want to force it
# if os.getenv("USE_SQLITE", "false").lower() == "true":
#     DATABASE_URL = "sqlite:///./questions.db"

# # Helper check to add connect_args for SQLite
# connect_args = {}
# if DATABASE_URL.startswith("sqlite"):
#     connect_args["check_same_thread"] = False

connect_args = {}
DATABASE_URL = "sqlite:///./questions.db"
connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
