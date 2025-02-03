from typing import List
from api.model import EventSchema, EventDB, EventPatch, RoleDB
from crud import roles
from api.crud_router import CRUDRouter
from db.model import Role


class RoleCRUDRouter(CRUDRouter[RoleDB]):
    def __init__(self):
        super().__init__(Role.__tablename__, roles.roles, RoleDB, RoleDB, RoleDB)


router = RoleCRUDRouter()
