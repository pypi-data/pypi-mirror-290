from typing import List, Optional, TypedDict
from optimodel_server_types import Credentials, ModelMessage, ModelTypes, Providers


class QueryResponse(TypedDict):
    """
    Response from a query to the provider
    """

    modelResponse: str
    promptTokens: int
    generationTokens: int
    cost: float
    provider: Providers
    guardErrors: List[str]


class QueryParams(TypedDict, total=False):
    messages: List[ModelMessage]
    model: ModelTypes
    temperature: float
    maxGenLen: Optional[int]
    credentials: Optional[List[Credentials]]
    jsonMode: Optional[bool]
