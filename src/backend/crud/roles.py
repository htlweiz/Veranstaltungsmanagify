from db.session import session, Session
from crud.crud import CRUD, log_db, select
from db.model import Role
from crud.classes import classes
from api.model import RoleDB


class RoleCRUD(CRUD[Role]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Role)


roles = RoleCRUD(session)
