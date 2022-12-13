from pydantic import BaseModel


class LocalFile(BaseModel):
    is_folder:bool
    last_modified:str
    file_path:str
    version:str