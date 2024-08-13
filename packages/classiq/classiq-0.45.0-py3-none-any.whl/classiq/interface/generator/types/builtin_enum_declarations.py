from enum import IntEnum

from classiq.interface.chemistry.elements import ELEMENTS
from classiq.interface.chemistry.ground_state_problem import FermionMapping
from classiq.interface.generator.types.enum_declaration import EnumDeclaration

ELEMENT = EnumDeclaration(
    name="Element", members={element: idx for idx, element in enumerate(ELEMENTS)}
)

FERMION_MAPPING = EnumDeclaration(
    name="FermionMapping",
    members={
        mapping.name: idx  # type:ignore[attr-defined]
        for idx, mapping in enumerate(FermionMapping)
    },
)


class FinanceFunctionType(IntEnum):
    VAR = 0
    SHORTFALL = 1
    X_SQUARE = 2
    EUROPEAN_CALL_OPTION = 3


class LadderOperator(IntEnum):
    PLUS = 0
    MINUS = 1


class Optimizer(IntEnum):
    COBYLA = 1
    SPSA = 2
    L_BFGS_B = 3
    NELDER_MEAD = 4
    ADAM = 5


class Pauli(IntEnum):
    I = 0  # noqa: E741
    X = 1
    Y = 2
    Z = 3


class QSVMFeatureMapEntanglement(IntEnum):
    FULL = 0
    LINEAR = 1
    CIRCULAR = 2
    SCA = 3
    PAIRWISE = 4


for enum_decl in list(vars().values()):
    if isinstance(enum_decl, EnumDeclaration):
        EnumDeclaration.BUILTIN_ENUM_DECLARATIONS[enum_decl.name] = enum_decl
    elif isinstance(enum_decl, type) and issubclass(enum_decl, IntEnum):
        EnumDeclaration.BUILTIN_ENUM_DECLARATIONS[enum_decl.__name__] = EnumDeclaration(
            name=enum_decl.__name__,
            members={enum_val.name: enum_val.value for enum_val in enum_decl},
        )
