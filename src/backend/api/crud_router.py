from typing import List, TypeVar, Generic, Type, Annotated
from crud import CRUD
from fastapi import APIRouter, Header, HTTPException, Request, status, Depends
from sqlalchemy import Select, select
from pydantic import BaseModel
from api.helpers import requires_user
from api.model import FilterModel
from sqlalchemy.orm import Query
from db.session import session


def paginate(query: Select, page: FilterModel):
    if page.limit < 0:
        raise ValueError("Limit value cannot be negative")
    if page.skip < 0:
        raise ValueError("Skip value cannot be negative")

    return query.limit(page.limit).offset(page.skip)


async def get_access_token(request: Request) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("access_token")
    if token == None:
        raise credentials_exception

    return token


V = TypeVar("V")  # Response-body type


class CRUDRouter(APIRouter, Generic[V]):
    def __init__(
        self,
        db_model_name: str,
        crud_model: CRUD,
        request_model: Type,
        response_model: Type[V],
        patch_model: Type,
        filter_model: Type = FilterModel,
        put_model: Type = BaseModel,
    ):
        if put_model is None:
            put_model = request_model
        super().__init__()
        self.model_name: str = db_model_name
        self.crud_model: CRUD = crud_model
        self.response_model: Type[V] = response_model

        async def read(filter: filter_model = Depends()) -> List[V]:
            return await self.read(filter)

        async def create(
            instance: request_model,
            AccessToken: Annotated[str | None, Depends(get_access_token)] = None,
        ):
            return await self.create(instance, AccessToken)

        async def put(
            id: int,
            instance: put_model,
            AccessToken: Annotated[str | None, Depends(get_access_token)] = None,
        ):
            return await self.put(id, instance, AccessToken)

        async def patch(
            id: int,
            instance: patch_model,
            cookie: Annotated[str | None, Depends(get_access_token)] = None,
        ):
            return await self.patch(id, instance, cookie)

        self.add_api_route(
            "/" + db_model_name,
            create,
            methods=["POST"],
            status_code=201,
            response_model=response_model,
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name,
            read,
            methods=["GET"],
            status_code=200,
            response_model=List[response_model],
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name + "/{id}",
            self.get_by_id,
            methods=["GET"],
            status_code=200,
            response_model=response_model,
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name + "/{id}",
            self.delete,
            methods=["DELETE"],
            status_code=204,
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name + "/{id}",
            put,
            methods=["PUT"],
            status_code=200,
            response_model=response_model,
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name + "/{id}",
            patch,
            methods=["PATCH"],
            status_code=200,
            response_model=response_model,
            tags=[db_model_name],
        )

    async def create(
        self, instance, AccessToken: Annotated[str | None, Header()] = None
    ):
        usr = requires_user(AccessToken)
        if usr is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        return self.crud_model.create(instance, usr.user_id)

    async def read(self, filter: BaseModel) -> List[V]:
        query = self.crud_model.read(filter)
        query = paginate(query, filter)
        result = session.execute(query).scalars().all()
        result = [self.response_model.model_validate(item) for item in result]
        return result

    async def delete(
        self, id: int, AccessToken: Annotated[str | None, Header()] = None
    ):
        usr = requires_user(AccessToken)
        if usr is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        self.crud_model.delete_by_id(id)

    async def get_by_id(self, id: int):
        return self.crud_model.get_by_id(id)

    async def put(
        self, id: int, instance, cookie: Annotated[str | None, Header()] = None
    ):
        return self.crud_model.put(id, instance)

    async def patch(
        self, id: int, instance, cookie: Annotated[str | None, Header()] = None
    ):
        return self.crud_model.patch(id, instance)
