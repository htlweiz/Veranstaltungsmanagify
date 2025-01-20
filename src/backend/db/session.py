import os

from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import sessionmaker
from db.model import Base


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