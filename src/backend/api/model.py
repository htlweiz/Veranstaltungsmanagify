from datetime import datetime
from typing import List, Optional, Type, Any, Tuple
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from copy import deepcopy


# Stolen from stackoverflow btw: https://stackoverflow.com/questions/67699451/make-every-field-as-optional-with-pydantic
def partial_model(model: Type[BaseModel]):
    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        },
    )


# end of steal


class SignupSchema(BaseModel):
    email: str
    password: str
    username: str

    def __str__(self) -> str:
        return f"Email: {self.email}, Password: {self.password}"


class LoginSchema(BaseModel):
    email: str
    password: str

    def __str__(self) -> str:
        return f"Email: {self.email}, Password: {self.password}"


class LoginDB(BaseModel):
    access_token: str

    def __str__(self) -> str:
        login_info = super().__str__()
        return f"User Token: {self.access_token}, {login_info}"

class MSALLogin(BaseModel):
    token: str

class UserSchema(BaseModel):
    email: str
    password: str
    username: str
    role: int

@partial_model
class UserPatch(UserSchema):
    pass

class UserDB(BaseModel):
    user_id: int
    role_id: int
    username: str
    email: str

class StudentSchema(BaseModel):
    first_name: str
    last_name: str
    is_female: bool
    class_name: str

class StudentDB(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    is_female: bool
    class_id: int 

class Address(BaseModel):
    street: str
    city: str
    country: str
    state: str
    zip: str

@partial_model
class AddressPatch(Address):
    pass

class EventSchema(BaseModel):
    start: datetime
    end: datetime
    curriculum_ref: str
    total_costs: int
    transportation_costs: int
    parental_info: bytes
    teachers: List[str]
    students: List[StudentSchema]
    address: Address

class MultiDayDataDB(BaseModel):
    sga_approved: Optional[bool] = None

class PendingApprovalDB(BaseModel):
    event_id: int
    user_id: int
    is_approved: bool


class EventDB(BaseModel):
    event_id: int
    start: datetime
    end: datetime
    curriculum_ref: str
    total_costs: int
    transportation_costs: int
    users: List[UserDB]
    students: List[StudentDB]
    address: Address
    multi_day_data: Optional[MultiDayDataDB] = None
    pending_approval: List[PendingApprovalDB]

@partial_model
class EventPatch(EventSchema):
    address: AddressPatch