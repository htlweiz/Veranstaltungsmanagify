from typing import List

from pydantic import BaseModel
from crud.crud import CRUD, log_db, select
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
import random
from datetime import timedelta
from sqlalchemy.sql import Select
from db.session import session, Session
from db.model import Event, Class, Student
from api.model import EventSchema, EventPatch, EventDB 
from sqlalchemy import and_ 
from crud.addresses import addresses
from crud.users import users
from db.model import UserApproveEvent, User
from crud.students import students
from crud.multi_day_events import multi_day_events


class EventCRUD(CRUD[Event]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Event)

    def create(self, payload: EventSchema, user_creating_id: int) -> EventDB:
        event = super().create(payload.model_dump(exclude={"teachers", "students", "address"}), user_creating_id) 
        address = addresses.create(payload.address, user_creating_id)
        teachers = [users.get_by_email(teacher) for teacher in payload.teachers]
        event_students = [students.get_by_id(student_id) for student_id in payload.students]

        event.address = address
        event.users = teachers
        event.students = event_students
        self.session.commit()

        user = session.get(User, user_creating_id)

        def create_pending_approval(user: User):
            if user.role.parent != None:
                available_approvers = session.query(User).where(User.role_id == user.role.parent.role_id).all()
                if len(available_approvers) == 0:
                    return

                random.shuffle(available_approvers)
                parent: User = available_approvers[0]

                pending_approval = UserApproveEvent(event_id=event.event_id, user_id=user.user_id, is_approved=False)
                session.add(pending_approval)
                create_pending_approval(parent)

        create_pending_approval(user)
        session.commit()

        if payload.end - payload.start > timedelta(days=1):
            multi_day_events.create(event.event_id, user_creating_id)

        pending_approval = session.query(UserApproveEvent).where(and_(UserApproveEvent.event_id == event.event_id, UserApproveEvent.is_approved == False)).all()
        event.pending_approval = pending_approval

        return event
    
    def patch(self, id, request: EventPatch) -> EventDB:
        event = super().patch(id, request.model_dump(exclude={"teachers", "students", "address"})) 
        if event is None:
            return None

        if request.address is not None:
            event.address = addresses.create(request.address, None)
        
        if request.teachers is not None:
            event.users = [users.get_by_email(teacher) for teacher in request.teachers]
        
        if request.students is not None:
            event.students = [students.get_by_id(student_id) for student_id in request.students]

        self.session.commit()

        # Update for multi-day event check
        # if request.end - request.start > timedelta(days=1):
        #    multi_day_events.create(event.event_id, None)
        return event

    def put(self, id, request):
        return self.patch(id, request)

events = EventCRUD(session)
