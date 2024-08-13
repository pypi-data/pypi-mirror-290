from typing import ClassVar, Dict, Optional, Sequence

import pydantic

from classiq.interface.generator.functions.concrete_types import ConcreteClassicalType
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)


class ClassicalFunctionDeclaration(FunctionDeclaration):
    """
    Facilitates the creation of a common classical function interface object.
    """

    name: str

    positional_parameters: Sequence[ClassicalParameterDeclaration] = pydantic.Field(
        default_factory=list,
    )

    return_type: Optional[ConcreteClassicalType] = pydantic.Field(
        description="The type of the classical value that is returned by the function (for classical functions)",
        default=None,
    )

    BUILTIN_FUNCTION_DECLARATIONS: ClassVar[
        Dict[str, "ClassicalFunctionDeclaration"]
    ] = {}

    FOREIGN_FUNCTION_DECLARATIONS: ClassVar[
        Dict[str, "ClassicalFunctionDeclaration"]
    ] = {}

    @property
    def param_decls(self) -> Sequence[ClassicalParameterDeclaration]:
        return self.positional_parameters


ClassicalFunctionDeclaration.update_forward_refs()
