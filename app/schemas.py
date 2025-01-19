from pydantic import BaseModel

from pydantic import BaseModel
from typing import List, Literal


class RecommendedAction(BaseModel):
    """Represents each recommended action with UI-related fields"""
    header: str
    text: str
    buttonText: str
    iconType: str


class Metric(BaseModel):
    """Represents each metric associated with a result"""
    unit: str
    label: str
    status: Literal["normal", "high", "low"]
    description: str


class Result(BaseModel):
    """Represents each result item in the results array"""
    value: str
    updatedAt: str
    title: str
    summary: str
    recommendedActions: List[RecommendedAction]
    suggestedQuestions: List[str]
    metrics: List[Metric]


class ChatRequest(BaseModel):
    message: str
    result: Result
