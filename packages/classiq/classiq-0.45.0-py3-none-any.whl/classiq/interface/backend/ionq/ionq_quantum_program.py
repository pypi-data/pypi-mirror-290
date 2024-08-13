from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

import pydantic
from pydantic import BaseModel

# This file is based on autogenerated code from: https://static.ionq.co/schemas/circuit-v0.json using
# https://pydantic-docs.helpmanual.io/datamodel_code_generator/
# Run: datamodel-codegen --url https://static.ionq.co/schemas/circuit-v0.json

if TYPE_CHECKING:
    PydanticGateName = str
else:
    PydanticGateName = pydantic.constr(
        regex=r"^\w+$",
        min_length=1,
    )


class Gate(BaseModel):
    gate: PydanticGateName
    target: Optional[int] = None
    control: Optional[int] = None
    targets: Optional[List[int]] = None
    controls: Optional[List[int]] = None

    # Ionq changes format sometimes.
    #   One example is that `IonqQauntumCircuit` got a field name "gateset" with the value "qis"
    #   Another is that `Gate` got a field named "rotation"
    class Config:
        extra = pydantic.Extra.allow


class IonqQuantumCircuit(BaseModel):
    qubits: int
    circuit: List[Gate]

    # Ionq changes format sometimes.
    #   One example is that `IonqQuantumCircuit` got a field name "gateset" with the value "qis"
    #   Another is that `Gate` got a field named "rotation"
    class Config:
        extra = pydantic.Extra.allow

    @classmethod
    def from_string(cls, code: str) -> IonqQuantumCircuit:
        code_lines = code.split(sep="\n")
        commentless_code = "\n".join(
            line for line in code_lines if not line.startswith("//")
        )
        return cls.parse_raw(commentless_code)
