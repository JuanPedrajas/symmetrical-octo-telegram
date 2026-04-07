from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str = ""


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = {"from_attributes": True}
