from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    username:str
    is_logged:Optional[bool] = True
    access_token:str