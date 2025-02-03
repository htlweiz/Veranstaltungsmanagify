from typing import List

from pydantic import BaseModel
from crud.crud import CRUD, log_db, select
from sqlalchemy.sql import Select
from db.session import session, Session
from db.model import Event, Class, Student, MultiDayEvent
from api.model import EventSchema, EventPatch, EventDB, StudentSchema
from sqlalchemy import and_ 
from crud.addresses import addresses
from crud.users import users
from crud.classes import classes

class MultiDayEventSchema(BaseModel):
    event_id: int
    sga_approved: bool = False

class MultiDayEventCRUD(CRUD[MultiDayEvent]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, MultiDayEvent)
    
    def create(self, payload: int, user_creating_id: int) -> MultiDayEvent:
        return super().create(MultiDayEventSchema(event_id=payload), user_creating_id)
 

multi_day_events = MultiDayEventCRUD(session)