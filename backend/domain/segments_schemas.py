from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class RecordSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    loom: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    pattern: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    right_rate: FiniteFloat
    left_rate: FiniteFloat
    pause: FiniteFloat


class VerifySegment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    segment: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
