from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    LargeBinary
)
from sqlalchemy.orm import declarative_base, relationship, Mapped, backref
from typing import List
from sqlalchemy import func


Base = declarative_base()

class UserBase:
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))


class UserApproveEvent(Base):
    __tablename__ = "user_approve_event"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    is_approved = Column(Boolean, nullable=False)


class UserEvent(Base):
    __tablename__ = "user_event"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", backref=backref("user_events", cascade="all, delete-orphan"))
    event = relationship("Event", backref=backref("user_events", cascade="all, delete-orphan"))

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    username = Column(String, nullable=False, unique=True)

    approvals = relationship("Event", secondary="user_approve_event", back_populates="approving_users")
    events = relationship("Event", secondary="user_event", back_populates="users")

class MultiDayEvent(Base):
    __tablename__ = "multi_day_events"

    multi_day_event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    sga_approved = Column(Boolean, nullable=False)

    event = relationship("Event", backref=backref("multi_day_data", cascade="all, delete-orphan"))

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    curriculum_ref = Column(String, nullable=False)
    total_costs = Column(Integer, nullable=False)
    transportation_costs = Column(Integer, nullable=False)
    parental_info = Column(LargeBinary)
    address_id = Column(Integer, ForeignKey("addresses.address_id", ondelete="CASCADE"))

    approving_users = relationship("User", secondary="user_approve_event", back_populates="approvals")
    users = relationship("User", secondary="user_event", back_populates="events")
    students = relationship("Student", secondary="event_student", back_populates="events")

    address = relationship("Address")
    multi_day_data = relationship("MultiDayEvent", backref=backref("event", cascade="all, delete-orphan"))

class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    students = relationship("Student", backref=backref("my_class", cascade="all, delete-orphan"))

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_female = Column(Boolean, nullable=False)

    class_id = Column(Integer, ForeignKey("classes.class_id", ondelete="CASCADE"))

    my_class = relationship("Class", backref=backref("students", cascade="all, delete-orphan"))
    events = relationship("Event", secondary="event_student", back_populates="students")


class EventStudent(Base):
    __tablename__ = "event_student"

    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), primary_key=True)

    event = relationship("Event", backref=backref("students", cascade="all, delete-orphan"))
    student = relationship("Student", backref=backref("events", cascade="all, delete-orphan"))


class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip = Column(String, nullable=False)
