from sqlalchemy import Column, Integer, String, Text
from app.database import Base
from typing import Optional
from pydantic import BaseModel


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    source = Column(String(255), nullable=True)


# Pydantic schemas for request/response validation
class QuestionCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    source: Optional[str] = None


class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    source: Optional[str] = None


class QuestionOut(BaseModel):
    id: int
    question: str
    answer: str
    category: Optional[str] = None
    source: Optional[str] = None

    class Config:
        orm_mode = True
