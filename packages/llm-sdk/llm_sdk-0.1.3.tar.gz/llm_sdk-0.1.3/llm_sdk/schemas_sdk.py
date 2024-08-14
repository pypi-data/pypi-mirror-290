from pydantic import BaseModel
from typing import Optional


class ProviderModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    logo: Optional[str]
    provider_id: int
    req_integration_params: dict


class ModelCreatorModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    logo: Optional[str]
    creator_id: int


class ModelTypeModel(BaseModel):
    id: int
    name: str
    description: Optional[str]


class AvailableModelModel(BaseModel):
    id: int
    provider: ProviderModel
    creator: ModelCreatorModel
    model_type: ModelTypeModel
    name: str
    model_name: Optional[str]
    model_version: Optional[str]
    is_verified: bool
    cost_input_token: float
    cost_output_token: float
