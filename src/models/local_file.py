from pydantic import BaseModel


class LocalFile(BaseModel):
    object_id: str
    is_folder: bool
    file_name: str
    last_modified: str
    file_path: str
    version: str
