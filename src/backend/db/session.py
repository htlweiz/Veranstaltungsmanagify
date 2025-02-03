import os

from sqlalchemy import (
    create_engine,
    MetaData,
    event,
)
from sqlalchemy.orm import sessionmaker
from db.model import Base, Role


DATABASE_URL: str | None
if os.getenv("TEST_ENV") == "1":
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata: MetaData = Base.metadata


Session = sessionmaker(bind=engine)
session = Session()

def create_default_roles(target, conn, **kwargs):
    from db.model import Role
    from sqlalchemy.orm import Session

    with Session(conn) as sess:
        director = Role(name="director", can_approve=True)
        sess.add(director)
        av = Role(name="av", can_approve=True, parent=director)
        sess.add(av)
        teacher = Role(name="teacher", can_approve=False, parent=av)
        sess.add(teacher)

        sess.commit()

    print("Default roles created")

event.listen(Role.__table__, "after_create", create_default_roles)