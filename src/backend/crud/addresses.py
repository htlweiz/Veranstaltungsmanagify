from typing import List
from crud.crud import CRUD, log_db, select
from sqlalchemy.sql import Select
from db.session import session, Session
from db.model import Address
from sqlalchemy import and_ 



class AddressCRUD(CRUD[Address]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Address)


addresses = AddressCRUD(session)