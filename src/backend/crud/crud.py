
import logging
from typing import Generic, List, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import Select
from db.session import metadata
from sqlalchemy.schema import Table
from functools import lru_cache 


def log_db(*args, **kwargs):
    object_name = kwargs.pop("class_name", "")
    action_tmp = kwargs.pop("action", "")

    def inner(f):
        def wrapper(*args, **kwargs):
            try:
                payload = str(args[1])
            except:
                payload = ""

            action = action_tmp
            if action_tmp == "":
                action = " ".join(f.__name__.capitalize().split("_"))
            logging.info(
                f"Performing Action: {action} on {object_name} with {'no' if payload == '' else payload} data ({payload})"
            )
            result = f(*args, **kwargs)
            logging.info(f"Successfully performed action {action} on {object_name}")
            return result

        return wrapper

    return inner


T = TypeVar("T", bound=BaseModel)


def validate(func):
    def wrapper(self, *args, **kwargs) -> T:
        payload_position = None
        for i, arg in enumerate(args):
            if isinstance(arg, BaseModel):
                payload_position = i
                break

        if payload_position is not None:
            payload = args[payload_position]
            user_creating_id = kwargs.get("user_creating_id", None)
            id = kwargs.get("id", None)
            if not self._validate(payload, id=id, user_creating_id=user_creating_id):
                raise RuntimeError("Validation Failed")

        return func(self, *args, **kwargs)

    return wrapper


class CRUD(Generic[T]):
    def __init__(self, session: Session, type: Type[T] = T) -> None:
        self.type = type
        self.session = session

    def _validate(
        self, payload: BaseModel, id: int = None, user_creating_id: int = None
    ) -> bool:
        return True

    @log_db(class_name=T.__name__)
    @validate
    def create(self, payload: BaseModel, user_creating_id: int) -> T:
        instance: T
        with self.session.begin_nested():
            instance = self.type(**dict(payload))
            instance.user_id = user_creating_id
            self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    @log_db(class_name=T.__name__)
    @validate
    def read(self, filter: BaseModel | None = None) -> Select[T]:
        _ = filter
        return select(self.type)

    @log_db(class_name=T.__name__)
    def delete(self, instance: T):
        with self.session.begin_nested():
            self.session.delete(instance)

    @log_db(class_name=T.__name__)
    def delete_by_id(self, instance_id: int):
        instance = self.get_by_id(instance_id)
        if instance == None:
            raise RuntimeError("Instance was not found")
        self.delete(instance)

    @log_db(class_name=T.__name__, action="Read by id")
    def get_by_id(self, id: int) -> T | None:
        return self.session.query(self.type).get(id)

    @log_db(class_name=T.__name__)
    @validate
    def put(self, id: int, request: BaseModel) -> T:
        instance = self.session.get(self.type, id)

        with self.session.begin_nested():
            data: dict = request.model_dump()
            for key, value in data.items():
                try:
                    setattr(instance, key, value)
                except:
                    pass
        self.refresh(instance)
        return instance

    @log_db(class_name=T.__name__)
    @validate
    def patch(self, id: int, request: BaseModel) -> T:
        instance = self.session.get(self.type, id)

        with self.session.begin_nested():
            data: dict = request.model_dump(exclude_unset=True, exclude_none=True)
            for key, value in data.items():
                try:
                    setattr(instance, key, value)
                except:
                    pass

        self.refresh(instance)
        return instance

    @log_db(class_name=T.__name__)
    def save(self):
        self.session.commit()

    def refresh(self, instance: T) -> T:
        self.session.refresh(instance)
        return instance
