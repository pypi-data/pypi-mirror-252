from pydantic import BaseModel, Field

from typing import List, Optional, Dict, Any
from humps import camelize


def to_camel(string):
    return camelize(string)


class GenerationParams(BaseModel):
    messages: Optional[List[Any]] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    user: Optional[str] = None
    prompt: Optional[str] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    functions: Optional[List[Any]] = None
    function_call: Optional[dict] = None
    tools: Optional[List[Any]] = None


class ModelGenerationRequest(BaseModel):
    model_name: str
    provider_name: str
    order: int = Field(int)
    prompt_params: Optional[GenerationParams] = Field(default={})

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        protected_namespaces = ()


class Usage(BaseModel):
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class Choice(BaseModel):
    index: int
    text: str
    finish_reason: str
    role: Optional[str] = None
    function_call: Optional[Any] = None


class GenerationResponse(BaseModel):
    id: str
    choices: List[Choice]
    model: str
    provider_id: Optional[str] = Field(None, alias="providerId")
    model_id: Optional[str] = Field(None, alias="modelId")
    meta: Optional[Usage]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        protected_namespaces = ()


class ChunkedGenerationResponse(BaseModel):
    event: str
    data: dict
