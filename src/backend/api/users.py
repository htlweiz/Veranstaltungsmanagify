from api.model import UserDB, UserPatch, UserSchema
from crud.users import users
from api.crud_router import CRUDRouter
from db.model import User


class UserCRUDRouter(CRUDRouter[UserDB]):
    def __init__(self):
        super().__init__(User.__tablename__, users, UserSchema, UserDB, UserPatch)


router = UserCRUDRouter()