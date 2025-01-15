from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    default_duration = Column(Integer)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    asap_tasks = relationship("AsapTask", back_populates="user", cascade="all, delete-orphan")
    command_history = relationship("CommandHistory", back_populates="user", cascade="all, delete-orphan")

class CommandHistory(Base):
    __tablename__ = "command_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    command = Column(String(255), nullable=False)

    user = relationship("User", back_populates="command_history")

class PriorityLevel(Base):
    __tablename__ = "priority_levels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    priority_level_id = Column(Integer, ForeignKey("priority_levels.id", ondelete="RESTRICT"))
    name = Column(String(255), nullable=False)
    duration = Column(Integer)
    due_date = Column(Date)
    rhythm = Column(Integer)

    user = relationship("User", back_populates="tasks")
    priority_level = relationship("PriorityLevel")

class AsapTask(Base):
    __tablename__ = "asap_tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="asap_tasks")