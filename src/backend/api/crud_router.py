from typing import TypeVar, Generic, Type, Annotated
from crud import CRUD
from fastapi import APIRouter, Header, HTTPException, status, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from pydantic import BaseModel
from api.helpers import requires_user


V = TypeVar("V")  # Response-body type


class CRUDRouter(APIRouter, Generic[V]):
    def __init__(
        self,
        db_model_name: str,
        crud_model: CRUD,
        request_model: Type,
        response_model: Type[V],
        patch_model: Type,
        filter_model: Type = BaseModel,
        put_model: Type = BaseModel,
    ):
        if put_model is None:
            put_model = request_model
        super().__init__()
        self.model_name: str = db_model_name
        self.crud_model: CRUD = crud_model

        async def read(filter: filter_model = Depends()):
            return await self.read(filter)

        async def create(
            instance: request_model, AccessToken: Annotated[str | None, Header()] = None
        ):
            return await self.create(instance, AccessToken)

        async def put(
            id: int,
            instance: put_model,
            AccessToken: Annotated[str | None, Header()] = None,
        ):
            return await self.put(id, instance, AccessToken)

        async def patch(
            id: int,
            instance: patch_model,
            cookie: Annotated[str | None, Header()] = None,
        ):
            return await self.patch(id, instance, cookie)

        self.add_api_route(
            "/" + db_model_name, create, methods=["POST"], status_code=201, response_model=response_model,
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name,
            read,
            methods=["GET"],
            status_code=200,
            response_model=Page[response_model],
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
            "/" + db_model_name + "/{id}", put, methods=["PUT"], status_code=200, response_model=response_model,
            tags=[db_model_name],
        )
        self.add_api_route(
            "/" + db_model_name + "/{id}", patch, methods=["PATCH"], status_code=200, response_model=response_model,
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

    async def read(self, filter: BaseModel) -> Page[V]:
        query = self.crud_model.read(filter)
        res = paginate(query=query, conn=self.crud_model.session)
        return res

    async def delete(
        self, id: int, AccessToken: Annotated[str | None, Header()] = None
    ):
        usr = requires_user(AccessToken)
        if usr is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        self.crud_model.delete_by_id(id)

    async def get_by_id(
        self, id: int
    ):
        return self.crud_model.get_by_id(id)

    async def put(
        self, id: int, instance, cookie: Annotated[str | None, Header()] = None
    ):
        return self.crud_model.put(id, instance)

    async def patch(
        self, id: int, instance, cookie: Annotated[str | None, Header()] = None
    ):
        return self.crud_model.patch(id, instance)