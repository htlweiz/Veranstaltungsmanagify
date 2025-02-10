from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination  # TODO: Use sqlalchemy pagination instead
from fastapi.middleware.cors import CORSMiddleware
from db.session import metadata, engine
from db.model import *
from fastapi import APIRouter
import logging
from api import auth, events, roles, users, students
from api.settings import ORIGINS


app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: \t %(message)s - %(asctime)s",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(roles.router)


add_pagination(app)
