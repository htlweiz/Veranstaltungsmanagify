from typing import Annotated
from fastapi import Header
from api.model import StudentDB, StudentSchema, StudentPatch
from crud.students import students
from api.crud_router import CRUDRouter
from db.model import Student


class StudentCRUDRouter(CRUDRouter[StudentDB]):
    def __init__(self):
        super().__init__(Student.__tablename__, students, StudentSchema, StudentDB, StudentPatch)
    
router = StudentCRUDRouter()