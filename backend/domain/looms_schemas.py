from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class SignMapping(BaseModel):
    model_config = ConfigDict(extra="forbid")
    loom: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    mapping_note: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
