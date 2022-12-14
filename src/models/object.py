from pydantic import BaseModel
from .user import User
from typing import List


class ObjectBase(BaseModel):
    is_folder: bool
    modified: str
    file_name: str
    file_extension: str
    file_size: int
    file_path: str
    is_starred: bool
    access_list: List[User]
    user: User


class ObjectCreate(ObjectBase):
    pass


class ObjectUpdate(BaseModel):
    object_id: str
    is_starred: bool
