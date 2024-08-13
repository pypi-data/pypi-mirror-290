from typing import Any, Dict, Literal

import pydantic

from classiq.interface.generator.functions.concrete_types import ConcreteClassicalType
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator
from classiq.interface.model.parameter import Parameter


class AnonClassicalParameterDeclaration(Parameter):
    kind: Literal["ClassicalParameterDeclaration"]

    classical_type: ConcreteClassicalType

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(
            values, "kind", "ClassicalParameterDeclaration"
        )

    def rename(self, new_name: str) -> "ClassicalParameterDeclaration":
        return ClassicalParameterDeclaration(**{**self.__dict__, "name": new_name})


class ClassicalParameterDeclaration(AnonClassicalParameterDeclaration):
    name: str
