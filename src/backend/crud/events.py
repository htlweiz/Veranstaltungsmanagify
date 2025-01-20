from typing import List

from pydantic import BaseModel
from crud.crud import CRUD, log_db, select
from datetime import timedelta
from sqlalchemy.sql import Select
from db.session import session, Session
from db.model import Event, Class, Student
from api.model import EventSchema, EventPatch, EventDB
from sqlalchemy import and_ 
from crud.addresses import addresses
from crud.users import users
from crud.students import students
from crud.multi_day_events import multi_day_events


class EventCRUD(CRUD[Event]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Event)

    def create(self, payload: EventSchema, user_creating_id: int) -> EventDB:
        event = super().create(payload, user_creating_id) 
        address = addresses.create(payload.address, user_creating_id)
        teachers = [users.get_by_email(teacher) for teacher in payload.teachers]
        event_students = [students.create(student, user_creating_id) for student in payload.students]

        event.address = address
        event.users = teachers
        event.students = event_students
        self.session.commit()

        if payload.end - payload.start > timedelta(days=1):
            multi_day_events.create(event.event_id, user_creating_id)
        
        return event
        

events = EventCRUD(session)
