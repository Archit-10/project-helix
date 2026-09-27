from pydantic import BaseModel


class VersionResponse(BaseModel):
    project_name: str
    version: str
    environment: str
