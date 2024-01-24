from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorIncidents


class GetValidatorIncidents(BaseModel):
    validator_incidents: List["GetValidatorIncidentsValidatorIncidents"] = Field(
        alias="validatorIncidents"
    )


class GetValidatorIncidentsValidatorIncidents(ValidatorIncidents):
    pass


GetValidatorIncidents.model_rebuild()
GetValidatorIncidentsValidatorIncidents.model_rebuild()
