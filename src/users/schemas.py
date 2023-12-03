from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BaseUser(BaseModel):
    name: str
    username: str
    family_name: str


class UserDetails(BaseUser):
    id: int


class UpdateUser(BaseModel):
    name: Optional[str] = Field(None)
    username: Optional[str] = Field(None)
    family_name: Optional[str] = Field(None)


class CreateUser(BaseUser):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    password: str
