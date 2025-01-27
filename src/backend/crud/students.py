from typing import List

from pydantic import BaseModel
from crud.crud import CRUD, log_db, select
from sqlalchemy.sql import Select
from db.session import session, Session
from db.model import Event, Class, Student
from api.model import EventSchema, EventPatch, EventDB, StudentSchema
from sqlalchemy import and_ 
from crud.addresses import addresses
from crud.users import users
from crud.classes import classes


class StudentCRUD(CRUD[Student]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Student)
    
    def create(self, payload: StudentSchema, user_creating_id: int) -> Student:
        student: Student = super().create(payload, user_creating_id)
        student_class = classes.get_or_create_by_class_name(payload.class_name)

        student.my_class = student_class
        self.session.commit()
        return student


students = StudentCRUD(session)