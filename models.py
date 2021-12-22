from collections import UserList
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Integer,
    String,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import create_session, relation, relationship
import datetime

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    phone_number = Column(String(50))
    current_state = Column(String(50))
    default_state = Column(String(50), default="UndefinedKoala")
    last_sended_message_id = Column(Integer)
    onboarding_page = Column(Integer, default=1)
    current_word_id = Column(String(50))
    questions = relationship("Question", backref="customer")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    text = Column(String(121))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="unanswered")

class Card(Base):
    __tablename__ = "card"
    id = Column(Integer, primary_key=True, autoincrement=True)
    correct_answer = Column(String(121))
    text = Column(String(121)) 
    image_path = Column(String(300))


class Lesson(Base): 
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    title = Column(String(300))


engine = create_engine('sqlite:///users.db')  # используя относительный путь

Base.metadata.create_all(engine)
