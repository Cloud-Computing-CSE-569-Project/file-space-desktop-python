from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    limit_quota: int
    profile_photo: str
    quota_used: int
    desktop: str
