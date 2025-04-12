from pydantic import BaseModel


class ConfigEntity(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    value: str
