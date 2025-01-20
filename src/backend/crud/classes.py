from typing import List

from pydantic import BaseModel
from crud.crud import CRUD, log_db, select
from sqlalchemy.sql import Select
from db.session import session, Session
from sqlalchemy.exc import IntegrityError
from db.model import Event, Class, Student
from api.model import EventSchema, EventPatch, EventDB
from sqlalchemy import and_ 
from crud.addresses import addresses
from crud.users import users


class ClassCRUD(CRUD[Class]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Class)
    
    def get_or_create_by_class_name(self, class_name: str) -> Class:
        instance = self.session.query(Class).filter_by(name=class_name).first()
        if instance:
            return instance
        else:
            instance = Class(name=class_name)
            self.session.add(instance)
            self.session.commit()
            return instance


classes = ClassCRUD(session)
