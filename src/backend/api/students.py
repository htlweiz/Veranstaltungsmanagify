from typing import Annotated
from fastapi import Header
from api.model import StudentDB, StudentSchema, StudentPatch
from crud.users import users
from api.crud_router import CRUDRouter
from db.model import Student


class StudentCRUDRouter(CRUDRouter[StudentDB]):
    def __init__(self):
        super().__init__(Student.__tablename__, users, StudentSchema, StudentDB, StudentPatch)
    
router = StudentCRUDRouter()