import inspect
from abc import ABC
from dataclasses import is_dataclass
from enum import Enum as PythonEnum
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Type,
    Union,
    cast,
    overload,
)

from sympy import Basic
from typing_extensions import Self

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.concrete_types import PythonClassicalTypes
from classiq.interface.model.classical_parameter_declaration import (
    AnonClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import AnonPortDeclaration
from classiq.interface.model.quantum_function_call import (
    ArgValue,
    OperandIdentifier,
    QuantumFunctionCall,
)
from classiq.interface.model.quantum_function_declaration import (
    AnonPositionalArg,
    AnonQuantumFunctionDeclaration,
    AnonQuantumOperandDeclaration,
    QuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.quantum_type import QuantumType
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.source_reference import SourceReference

from classiq.qmod.model_state_container import QMODULE, ModelStateContainer
from classiq.qmod.qmod_constant import QConstant
from classiq.qmod.qmod_parameter import (
    CInt,
    CParam,
    CParamScalar,
    create_param,
    get_qmod_type,
)
from classiq.qmod.qmod_variable import (
    QVar,
    create_qvar_for_port_decl,
    set_symbolic_qvar_properties,
)
from classiq.qmod.quantum_callable import QCallable, QExpandableInterface
from classiq.qmod.symbolic_expr import SymbolicExpr
from classiq.qmod.type_attribute_remover import decl_without_type_attributes
from classiq.qmod.utilities import mangle_keyword, qmod_val_to_expr_str

ArgType = Union[CParam, QVar, QCallable]


class QExpandable(QCallable, QExpandableInterface, ABC):
    STACK: ClassVar[List["QExpandable"]] = list()

    def __init__(self, py_callable: Callable) -> None:
        self._qmodule: ModelStateContainer = QMODULE
        self._py_callable: Callable = py_callable
        self._body: List[QuantumStatement] = list()

    @property
    def body(self) -> List[QuantumStatement]:
        return self._body

    def __enter__(self) -> Self:
        QExpandable.STACK.append(self)
        QCallable.CURRENT_EXPANDABLE = self
        self._body.clear()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        assert QExpandable.STACK.pop() is self
        QCallable.CURRENT_EXPANDABLE = (
            QExpandable.STACK[-1] if QExpandable.STACK else None
        )

    def expand(self) -> None:
        if self not in QExpandable.STACK:
            with self, set_symbolic_qvar_properties(True):
                self._py_callable(*self._get_positional_args())

    def infer_rename_params(self) -> Optional[List[str]]:
        return None

    def add_local_handle(
        self,
        name: str,
        qtype: QuantumType,
        source_ref: Optional[SourceReference] = None,
    ) -> None:
        self._body.append(
            VariableDeclarationStatement(
                name=name, quantum_type=qtype, source_ref=source_ref
            )
        )

    def append_statement_to_body(self, stmt: QuantumStatement) -> None:
        self._body.append(stmt)

    def _get_positional_args(self) -> List[ArgType]:
        result: List[ArgType] = []
        for idx, arg in enumerate(self.func_decl.positional_arg_declarations):
            rename_params = self.infer_rename_params()
            actual_name = (
                rename_params[idx] if rename_params is not None else arg.get_name()
            )
            if isinstance(arg, AnonClassicalParameterDeclaration):
                result.append(
                    create_param(actual_name, arg.classical_type, self._qmodule)
                )
            elif isinstance(arg, AnonPortDeclaration):
                result.append(create_qvar_for_port_decl(arg, actual_name))
            else:
                assert isinstance(arg, AnonQuantumOperandDeclaration)
                result.append(QTerminalCallable(arg, idx))
        return result

    def create_quantum_function_call(
        self, source_ref_: SourceReference, *args: Any, **kwargs: Any
    ) -> QuantumFunctionCall:
        func_decl = self.func_decl
        if not isinstance(func_decl, QuantumFunctionDeclaration):
            raise NotImplementedError
        return _create_quantum_function_call(
            func_decl, None, source_ref_, *args, **kwargs
        )


class QLambdaFunction(QExpandable):
    def __init__(
        self, decl: AnonQuantumFunctionDeclaration, py_callable: Callable
    ) -> None:
        py_callable.__annotations__.pop("return", None)
        super().__init__(py_callable)
        self._decl = decl

    @property
    def func_decl(self) -> AnonQuantumFunctionDeclaration:
        return self._decl

    def infer_rename_params(self) -> List[str]:
        return inspect.getfullargspec(self._py_callable).args


class QTerminalCallable(QCallable):
    @overload
    def __init__(
        self,
        decl: QuantumFunctionDeclaration,
        param_idx: Optional[int] = None,
        index_: Optional[Union[int, CParamScalar]] = None,
    ) -> None:
        pass

    @overload
    def __init__(
        self,
        decl: AnonQuantumFunctionDeclaration,
        param_idx: int,
        index_: Optional[Union[int, CParamScalar]] = None,
    ) -> None:
        pass

    def __init__(
        self,
        decl: AnonQuantumFunctionDeclaration,
        param_idx: Optional[int] = None,
        index_: Optional[Union[int, CParamScalar]] = None,
    ) -> None:
        self._decl = self._override_decl_name(decl, param_idx)
        self._index = index_

    @staticmethod
    def _override_decl_name(
        decl: AnonQuantumFunctionDeclaration, param_idx: Optional[int]
    ) -> QuantumFunctionDeclaration:
        if (
            not isinstance(QCallable.CURRENT_EXPANDABLE, QLambdaFunction)
            or param_idx is None
        ):
            return decl.rename(decl.get_name())
        rename_params = QCallable.CURRENT_EXPANDABLE.infer_rename_params()
        return decl.rename(new_name=rename_params[param_idx])

    @property
    def is_list(self) -> bool:
        return (
            isinstance(self._decl, AnonQuantumOperandDeclaration) and self._decl.is_list
        )

    def __getitem__(self, key: Union[slice, int, CInt]) -> "QTerminalCallable":
        if not self.is_list:
            raise ClassiqValueError("Cannot index a non-list operand")
        if isinstance(key, slice):
            raise NotImplementedError("Operand lists don't support slicing")
        if isinstance(key, CParam) and not isinstance(key, CParamScalar):
            raise ClassiqValueError("Non-classical parameter for slicing")
        return QTerminalCallable(self._decl, index_=key)

    def __len__(self) -> int:
        raise ClassiqValueError(
            "len(<func>) is not supported for quantum callables - use <func>.len instead (Only if it is an operand list)"
        )

    if TYPE_CHECKING:

        @property
        def len(self) -> int: ...

    else:

        @property
        def len(self) -> CParamScalar:
            if not self.is_list:
                raise ClassiqValueError("Cannot get length of a non-list operand")
            return CParamScalar(f"get_field({self.func_decl.name}, 'len')")

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        return self._decl

    def create_quantum_function_call(
        self, source_ref_: SourceReference, *args: Any, **kwargs: Any
    ) -> QuantumFunctionCall:
        if self.is_list and self._index is None:
            raise ClassiqValueError(
                f"Quantum operand {self.func_decl.name!r} is a list and must be indexed"
            )
        return _create_quantum_function_call(
            self.func_decl, self._index, source_ref_, *args, **kwargs
        )


@overload
def prepare_arg(
    arg_decl: AnonPositionalArg,
    val: Union[QCallable, Callable[..., None]],
    func_name: Optional[str],
    param_name: str,
) -> QuantumLambdaFunction: ...


@overload
def prepare_arg(
    arg_decl: AnonPositionalArg, val: Any, func_name: Optional[str], param_name: str
) -> ArgValue: ...


def prepare_arg(
    arg_decl: AnonPositionalArg, val: Any, func_name: Optional[str], param_name: str
) -> ArgValue:
    if isinstance(val, QConstant):
        val.add_to_model()
        return Expression(expr=str(val.name))
    if isinstance(arg_decl, AnonClassicalParameterDeclaration):
        _validate_classical_arg(val, arg_decl, func_name)
        return Expression(expr=qmod_val_to_expr_str(val))
    elif isinstance(arg_decl, AnonPortDeclaration):
        if not isinstance(val, QVar):
            func_name_message = (
                "" if func_name is None else f" of function {func_name!r}"
            )
            raise ClassiqValueError(
                f"Argument {str(val)!r} to parameter {param_name!r}{func_name_message} "
                f"has incompatible type; expected quantum variable"
            )
        return val.get_handle_binding()
    else:
        if isinstance(val, list):
            if not all(isinstance(v, QCallable) or callable(v) for v in val):
                raise ClassiqValueError(
                    f"Quantum operand {param_name!r} cannot be initialized with a "
                    f"list of non-callables"
                )
            val = cast(List[Union[QCallable, Callable[[Any], None]]], val)
            return [prepare_arg(arg_decl, v, func_name, param_name) for v in val]

        if not isinstance(val, QCallable):
            new_arg_decl = decl_without_type_attributes(arg_decl)
            val = QLambdaFunction(new_arg_decl, val)
            val.expand()
            return QuantumLambdaFunction(
                pos_rename_params=val.infer_rename_params(),
                body=val.body,
            )

        if isinstance(val, QExpandable):
            val.expand()
        return val.func_decl.name


def _validate_classical_arg(
    arg: Any, arg_decl: AnonClassicalParameterDeclaration, func_name: Optional[str]
) -> None:
    if (
        not isinstance(
            arg, (*PythonClassicalTypes, CParam, SymbolicExpr, Basic, PythonEnum)
        )
        and not is_dataclass(arg)  # type:ignore[unreachable]
        or isinstance(arg, SymbolicExpr)
        and arg.is_quantum
    ):
        func_name_message = "" if func_name is None else f" of function {func_name!r}"
        raise ClassiqValueError(
            f"Argument {str(arg)!r} to parameter {arg_decl.name!r}{func_name_message} "
            f"has incompatible type; expected "
            f"{get_qmod_type(arg_decl.classical_type).__name__}"
        )


def _get_operand_hint_args(
    func: AnonQuantumFunctionDeclaration, param: AnonPositionalArg, param_value: str
) -> str:
    return ", ".join(
        [
            (
                f"{decl.name}={param_value}"
                if decl.name == param.name
                else f"{decl.name}=..."
            )
            for decl in func.positional_arg_declarations
        ]
    )


def _get_operand_hint(
    func: AnonQuantumFunctionDeclaration, param: AnonPositionalArg
) -> str:
    return (
        f"\nHint: To call a function under {func.name!r} use a lambda function as in "
        f"'{func.name}({_get_operand_hint_args(func, param, 'lambda: f(q)')})' "
        f"or pass the quantum function directly as in "
        f"'{func.name}({_get_operand_hint_args(func, param, 'f')})'."
    )


def _prepare_args(
    decl: AnonQuantumFunctionDeclaration, arg_list: List[Any], kwargs: Dict[str, Any]
) -> List[ArgValue]:
    result = []
    for idx, arg_decl in enumerate(decl.positional_arg_declarations):
        arg = None
        if arg_list:
            arg = arg_list.pop(0)
        elif arg_decl.name is not None:
            arg = kwargs.pop(mangle_keyword(arg_decl.name), None)
        if arg is None:
            if arg_decl.name is not None:
                param_name = repr(arg_decl.name)
            else:
                param_name = f"#{idx + 1}"
            error_message = f"Missing required argument for parameter {param_name}"
            if isinstance(arg_decl, AnonQuantumOperandDeclaration):
                error_message += _get_operand_hint(decl, arg_decl)
            raise ClassiqValueError(error_message)
        param_name = arg_decl.name if arg_decl.name is not None else f"#{idx + 1}"
        result.append(prepare_arg(arg_decl, arg, decl.name, param_name))

    return result


def _create_quantum_function_call(
    decl_: QuantumFunctionDeclaration,
    index_: Optional[Union[CParamScalar, int]] = None,
    source_ref_: Optional[SourceReference] = None,
    *args: Any,
    **kwargs: Any,
) -> QuantumFunctionCall:
    arg_decls = decl_.positional_arg_declarations
    arg_list = list(args)
    prepared_args = _prepare_args(decl_, arg_list, kwargs)

    if kwargs:
        bad_kwarg = next(iter(kwargs))
        if not all(arg_decl.name == bad_kwarg for arg_decl in arg_decls):
            raise ClassiqValueError(
                f"{decl_.name}() got an unexpected keyword argument {bad_kwarg!r}"
            )
        else:
            raise ClassiqValueError(
                f"{decl_.name}() got multiple values for argument {bad_kwarg!r}"
            )
    if arg_list:
        raise ClassiqValueError(
            f"{decl_.name}() takes {len(arg_decls)} arguments but {len(args)} were given"
        )
    function_ident: Union[str, OperandIdentifier] = decl_.name
    if index_ is not None:
        function_ident = OperandIdentifier(
            index=Expression(expr=str(index_)), name=function_ident
        )

    return QuantumFunctionCall(
        function=function_ident, positional_args=prepared_args, source_ref=source_ref_
    )
