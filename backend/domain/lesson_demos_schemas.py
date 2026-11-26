from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ReplaceDemo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    axis: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    loom: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    lesson: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    previous: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class RestoreDemo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    demo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    older: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
