from pydantic import BaseModel


class SyncFolder(BaseModel):
    id:str
    owner:str
    
