from typing import Any

from pydantic import BaseModel


class StepModel(BaseModel):
    keyword: str
    text: str


class ScenarioModel(BaseModel):
    name: str
    tags: list[str] = []
    steps: list[StepModel] = []


class FeatureDetail(BaseModel):
    feature: str
    description: str = ""
    tags: list[str] = []
    background: list[StepModel] = []
    scenarios: list[ScenarioModel] = []


class SaveRequest(BaseModel):
    path: str
    author: str
    data: FeatureDetail


class TreeResponse(BaseModel):
    tree: dict[str, Any]


class SaveResponse(BaseModel):
    status: str
    path: str
