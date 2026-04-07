from pydantic import BaseModel


class WordResponse(BaseModel):
    id: int
    text: str
    ipa: list[str]

    model_config = {"from_attributes": True}
