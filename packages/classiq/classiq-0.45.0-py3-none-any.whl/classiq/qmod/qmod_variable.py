import abc
import sys
from contextlib import contextmanager
from typing import (  # type: ignore[attr-defined]
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Generic,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    _GenericAlias,
    cast,
    get_args,
    get_origin,
)

from typing_extensions import Annotated, ParamSpec, Self, _AnnotatedAlias

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_qarray_proxy import (
    ILLEGAL_SLICE_BOUNDS_MSG,
    ILLEGAL_SLICE_MSG,
    ILLEGAL_SLICING_STEP_MSG,
    SLICE_OUT_OF_BOUNDS_MSG,
    SUBSCRIPT_OUT_OF_BOUNDS_MSG,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_name import TypeName
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.port_declaration import AnonPortDeclaration
from classiq.interface.model.quantum_expressions.amplitude_loading_operation import (
    AmplitudeLoadingOperation,
)
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    QuantumType,
)
from classiq.interface.source_reference import SourceReference

from classiq.qmod.model_state_container import QMODULE, ModelStateContainer
from classiq.qmod.qmod_parameter import ArrayBase, CBool, CInt, CParamScalar
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.symbolic_expr import Symbolic, SymbolicExpr
from classiq.qmod.symbolic_type import SymbolicTypes
from classiq.qmod.utilities import get_source_ref, version_portable_get_args

QVAR_PROPERTIES_ARE_SYMBOLIC = True


@contextmanager
def set_symbolic_qvar_properties(symbolic: bool) -> Iterator[None]:
    global QVAR_PROPERTIES_ARE_SYMBOLIC
    previous_symbolic = QVAR_PROPERTIES_ARE_SYMBOLIC
    QVAR_PROPERTIES_ARE_SYMBOLIC = symbolic
    yield
    QVAR_PROPERTIES_ARE_SYMBOLIC = previous_symbolic


def _is_input_output_typehint(type_hint: Any) -> bool:
    return isinstance(type_hint, _AnnotatedAlias) and isinstance(
        type_hint.__metadata__[0], PortDeclarationDirection
    )


def get_type_hint_expr(type_hint: Any) -> str:
    if isinstance(type_hint, ForwardRef):  # expression in string literal
        return str(type_hint.__forward_arg__)
    if get_origin(type_hint) == Literal:  # explicit numeric literal
        return str(get_args(type_hint)[0])
    else:
        return str(type_hint)  # implicit numeric literal


@contextmanager
def _no_current_expandable() -> Iterator[None]:
    current_expandable = QCallable.CURRENT_EXPANDABLE
    QCallable.CURRENT_EXPANDABLE = None
    try:
        yield
    finally:
        QCallable.CURRENT_EXPANDABLE = current_expandable


class QVar(Symbolic):
    def __init__(
        self,
        origin: Union[str, HandleBinding],
        *,
        expr_str: Optional[str] = None,
        depth: int = 2,
    ) -> None:
        super().__init__(str(origin), True)
        source_ref = (
            get_source_ref(sys._getframe(depth))
            if isinstance(origin, str)
            else origin.source_ref
        )
        self._base_handle: HandleBinding = (
            HandleBinding(name=origin) if isinstance(origin, str) else origin
        )
        if isinstance(origin, str) and QCallable.CURRENT_EXPANDABLE is not None:
            QCallable.CURRENT_EXPANDABLE.add_local_handle(
                origin, self.get_qmod_type(), source_ref
            )
        self._expr_str = expr_str if expr_str is not None else str(origin)

    def get_handle_binding(self) -> HandleBinding:
        return self._base_handle

    @abc.abstractmethod
    def get_qmod_type(self) -> QuantumType:
        raise NotImplementedError()

    @staticmethod
    def from_type_hint(type_hint: Any) -> Optional[Type["QVar"]]:
        if _is_input_output_typehint(type_hint):
            return QVar.from_type_hint(type_hint.__args__[0])
        type_ = get_origin(type_hint) or type_hint
        if issubclass(type_, QVar):
            if issubclass(type_, QStruct):
                with _no_current_expandable():
                    type_("DUMMY")._add_qmod_qstruct(qmodule=QMODULE)
            return type_
        return None

    @classmethod
    @abc.abstractmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def to_qvar(
        cls,
        origin: Union[str, HandleBinding],
        type_hint: Any,
        expr_str: Optional[str],
    ) -> Self:
        raise NotImplementedError()

    @classmethod
    def port_direction(cls, type_hint: Any) -> PortDeclarationDirection:
        if _is_input_output_typehint(type_hint):
            assert len(type_hint.__metadata__) >= 1
            return type_hint.__metadata__[0]
        assert type_hint == cls or get_origin(type_hint) == cls
        return PortDeclarationDirection.Inout

    def __str__(self) -> str:
        return self._expr_str

    @property
    def size(self) -> Union[CParamScalar, int]:
        if not QVAR_PROPERTIES_ARE_SYMBOLIC:
            return self._evaluate_size()
        return CParamScalar(f"get_field({self}, 'size')")

    @abc.abstractmethod
    def _evaluate_size(self) -> int:
        raise NotImplementedError


_Q = TypeVar("_Q", bound=QVar)
Output = Annotated[_Q, PortDeclarationDirection.Output]
Input = Annotated[_Q, PortDeclarationDirection.Input]


class QScalar(QVar, SymbolicExpr):
    def __init__(
        self,
        origin: Union[str, HandleBinding],
        *,
        _expr_str: Optional[str] = None,
        depth: int = 2,
    ) -> None:
        QVar.__init__(self, origin, expr_str=_expr_str, depth=depth)
        SymbolicExpr.__init__(self, str(origin), True)

    def _insert_arith_operation(
        self, expr: SymbolicTypes, inplace: bool, source_ref: SourceReference
    ) -> None:
        # Fixme: Arithmetic operations are not yet supported on slices (see CAD-12670)
        if TYPE_CHECKING:
            assert QCallable.CURRENT_EXPANDABLE is not None
        QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
            ArithmeticOperation(
                expression=Expression(expr=str(expr)),
                result_var=self.get_handle_binding(),
                inplace_result=inplace,
                source_ref=source_ref,
            )
        )

    def _insert_amplitude_loading(
        self, expr: SymbolicTypes, source_ref: SourceReference
    ) -> None:
        if TYPE_CHECKING:
            assert QCallable.CURRENT_EXPANDABLE is not None
        QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
            AmplitudeLoadingOperation(
                expression=Expression(expr=str(expr)),
                result_var=self.get_handle_binding(),
                source_ref=source_ref,
            )
        )

    def __ior__(self, other: Any) -> Self:
        if not isinstance(other, get_args(SymbolicTypes)):
            raise TypeError(
                f"Invalid argument {other!r} for out-of-place arithmetic operation"
            )

        self._insert_arith_operation(other, False, get_source_ref(sys._getframe(1)))
        return self

    def __ixor__(self, other: Any) -> Self:
        if not isinstance(other, get_args(SymbolicTypes)):
            raise TypeError(
                f"Invalid argument {other!r} for in-place arithmetic operation"
            )

        self._insert_arith_operation(other, True, get_source_ref(sys._getframe(1)))
        return self

    def __imul__(self, other: Any) -> Self:
        if not isinstance(other, get_args(SymbolicTypes)):
            raise TypeError(
                f"Invalid argument {other!r} for out of ampltiude encoding operation"
            )

        self._insert_amplitude_loading(other, get_source_ref(sys._getframe(1)))
        return self


class QBit(QScalar):
    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        return QuantumBit()

    @classmethod
    def to_qvar(
        cls,
        origin: Union[str, HandleBinding],
        type_hint: Any,
        expr_str: Optional[str],
    ) -> "QBit":
        return QBit(origin, _expr_str=expr_str)

    def get_qmod_type(self) -> QuantumType:
        return QuantumBit()

    def _evaluate_size(self) -> int:
        return 1


_P = ParamSpec("_P")


class QNum(Generic[_P], QScalar):
    def __init__(
        self,
        name: Union[str, HandleBinding],
        size: Union[int, CInt, Expression, None] = None,
        is_signed: Union[bool, CBool, Expression, None] = None,
        fraction_digits: Union[int, CInt, Expression, None] = None,
        _expr_str: Optional[str] = None,
    ):
        if (
            size is None
            and (is_signed is not None or fraction_digits is not None)
            or size is not None
            and (is_signed is None or fraction_digits is None)
        ):
            raise ClassiqValueError(
                "Assign none or all of size, is_signed, and fraction_digits"
            )
        self._size = (
            size
            if size is None or isinstance(size, Expression)
            else Expression(expr=str(size))
        )
        self._is_signed = (
            is_signed
            if is_signed is None or isinstance(is_signed, Expression)
            else Expression(expr=str(is_signed))
        )
        self._fraction_digits = (
            fraction_digits
            if fraction_digits is None or isinstance(fraction_digits, Expression)
            else Expression(expr=str(fraction_digits))
        )
        super().__init__(name, _expr_str=_expr_str, depth=3)

    @classmethod
    def _get_attributes(cls, type_hint: Any) -> Tuple[Any, Any, Any]:
        type_args = version_portable_get_args(type_hint)
        if len(type_args) == 0:
            return None, None, None
        if len(type_args) != 3:
            raise ClassiqValueError(
                "QNum receives three type arguments: QNum[size: int | CInt, "
                "is_signed: bool | CBool, fraction_digits: int | CInt]"
            )
        return type_args[0], type_args[1], type_args[2]

    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        size, is_signed, fraction_digits = cls._get_attributes(type_hint)
        return QuantumNumeric(
            size=(
                Expression(expr=get_type_hint_expr(size)) if size is not None else None
            ),
            is_signed=(
                Expression(expr=get_type_hint_expr(is_signed))
                if is_signed is not None
                else None
            ),
            fraction_digits=(
                Expression(expr=get_type_hint_expr(fraction_digits))
                if fraction_digits is not None
                else None
            ),
        )

    @classmethod
    def to_qvar(
        cls,
        origin: Union[str, HandleBinding],
        type_hint: Any,
        expr_str: Optional[str],
    ) -> "QNum":
        return QNum(origin, *cls._get_attributes(type_hint), _expr_str=expr_str)

    def get_qmod_type(self) -> QuantumType:
        return QuantumNumeric(
            size=self._size,
            is_signed=self._is_signed,
            fraction_digits=self._fraction_digits,
        )

    def _evaluate_size(self) -> int:
        if TYPE_CHECKING:
            assert self._size is not None
        return self._size.to_int_value()

    @property
    def fraction_digits(self) -> Union[CParamScalar, int]:
        if not QVAR_PROPERTIES_ARE_SYMBOLIC:
            if TYPE_CHECKING:
                assert self._fraction_digits is not None
            return self._fraction_digits.to_int_value()
        return CParamScalar(f"get_field({self}, 'fraction_digits')")

    @property
    def is_signed(self) -> Union[CParamScalar, bool]:
        if not QVAR_PROPERTIES_ARE_SYMBOLIC:
            if TYPE_CHECKING:
                assert self._is_signed is not None
            return self._is_signed.to_bool_value()
        return CParamScalar(f"get_field({self}, 'is_signed')")

    # Support comma-separated generic args in older Python versions
    if sys.version_info[0:2] < (3, 10):

        def __class_getitem__(cls, args) -> _GenericAlias:
            return _GenericAlias(cls, args)


class QArray(ArrayBase[_P], QVar):
    # TODO [CAD-18620]: improve type hints
    def __init__(
        self,
        name: Union[str, HandleBinding],
        element_type: Union[_GenericAlias, QuantumType] = QBit,
        length: Optional[Union[int, SymbolicExpr, Expression]] = None,
        _expr_str: Optional[str] = None,
    ) -> None:
        self._element_type = element_type
        self._length = (
            length
            if length is None or isinstance(length, Expression)
            else Expression(expr=str(length))
        )
        super().__init__(name, expr_str=_expr_str)

    def __getitem__(self, key: Union[slice, int, SymbolicExpr]) -> Any:
        return (
            self._get_slice(key) if isinstance(key, slice) else self._get_subscript(key)
        )

    def _get_subscript(self, index: Union[slice, int, SymbolicExpr]) -> Any:
        if isinstance(index, SymbolicExpr) and index.is_quantum:
            raise ClassiqValueError("Non-classical parameter for slicing")
        if (
            isinstance(index, int)
            and self._length is not None
            and self._length.is_evaluated()
        ):
            length = self._length.to_int_value()
            if index < 0 or index >= length:
                raise ClassiqValueError(SUBSCRIPT_OUT_OF_BOUNDS_MSG)

        return _create_qvar_for_qtype(
            self.get_qmod_type().element_type,
            SubscriptHandleBinding(
                base_handle=self._base_handle,
                index=Expression(expr=str(index)),
            ),
            expr_str=f"{self}[{index}]",
        )

    def _get_slice(self, slice_: slice) -> Any:
        if slice_.step is not None:
            raise ClassiqValueError(ILLEGAL_SLICING_STEP_MSG)
        if not isinstance(slice_.start, (int, SymbolicExpr)) or not isinstance(
            slice_.stop, (int, SymbolicExpr)
        ):
            raise ClassiqValueError(ILLEGAL_SLICE_MSG)
        if (
            isinstance(slice_.start, int)
            and isinstance(slice_.stop, int)
            and slice_.start >= slice_.stop
        ):
            raise ClassiqValueError(
                ILLEGAL_SLICE_BOUNDS_MSG.format(slice_.start, slice_.stop)
            )
        if self._length is not None and self._length.is_evaluated():
            length = self._length.to_int_value()
            if (
                isinstance(slice_.start, int)
                and slice_.start < 0
                or isinstance(slice_.stop, int)
                and slice_.stop > length
            ):
                raise ClassiqValueError(SLICE_OUT_OF_BOUNDS_MSG)

        return QArray(
            name=SlicedHandleBinding(
                base_handle=self._base_handle,
                start=Expression(expr=str(slice_.start)),
                end=Expression(expr=str(slice_.stop)),
            ),
            element_type=self._element_type,
            length=slice_.stop - slice_.start,
            _expr_str=f"{self}[{slice_.start}:{slice_.stop}]",
        )

    def __len__(self) -> int:
        raise ClassiqValueError(
            "len(<var>) is not supported for quantum variables - use <var>.len instead"
        )

    if TYPE_CHECKING:

        @property
        def len(self) -> int: ...

    else:

        @property
        def len(self) -> Union[CParamScalar, int]:
            if not QVAR_PROPERTIES_ARE_SYMBOLIC:
                return self._length.to_int_value()
            if self._length is not None:
                return CParamScalar(f"{self._length}")
            return CParamScalar(f"get_field({self}, 'len')")

    def _evaluate_size(self) -> int:
        if TYPE_CHECKING:
            assert self._length is not None
        return self._element_type.size_in_bits * self._length.to_int_value()

    @classmethod
    def _get_attributes(cls, type_hint: Any) -> Tuple[Type[QVar], Any]:
        type_args = version_portable_get_args(type_hint)
        if len(type_args) == 0:
            return QBit, None
        if len(type_args) == 1:
            if isinstance(type_args[0], (str, int)):
                return QBit, type_args[0]
            return type_args[0], None
        if len(type_args) != 2:
            raise ClassiqValueError(
                "QArray receives two type arguments: QArray[element_type: QVar, "
                "length: int | CInt]"
            )
        return cast(Tuple[Type[QVar], Any], type_args)

    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        api_element_type, length = cls._get_attributes(type_hint)
        api_element_class = get_origin(api_element_type) or api_element_type
        element_type = api_element_class.to_qmod_quantum_type(api_element_type)

        length_expr: Optional[Expression] = None
        if length is not None:
            length_expr = Expression(expr=get_type_hint_expr(length))

        return QuantumBitvector(element_type=element_type, length=length_expr)

    @classmethod
    def to_qvar(
        cls,
        origin: Union[str, HandleBinding],
        type_hint: Any,
        expr_str: Optional[str],
    ) -> "QArray":
        return QArray(origin, *cls._get_attributes(type_hint), _expr_str=expr_str)

    def get_qmod_type(self) -> QuantumBitvector:
        if isinstance(self._element_type, QuantumType):
            element_type = self._element_type
        else:
            element_class = get_origin(self._element_type) or self._element_type
            element_type = element_class.to_qmod_quantum_type(self._element_type)
        return QuantumBitvector(
            element_type=element_type,
            length=self._length,
        )


class QStruct(QVar):
    _struct_name: str
    _fields: Mapping[str, QVar]

    def __init__(
        self,
        name: Union[str, HandleBinding],
        _struct_name: Optional[str] = None,
        _fields: Optional[Mapping[str, QVar]] = None,
        _expr_str: Optional[str] = None,
    ) -> None:
        if _struct_name is None or _fields is None:
            with _no_current_expandable():
                temp_var = QStruct.to_qvar(name, type(self), _expr_str)
                _struct_name = temp_var._struct_name
                _fields = temp_var._fields
        self._struct_name = _struct_name
        self._fields = _fields
        for field_name, var in _fields.items():
            setattr(self, field_name, var)
        super().__init__(name)
        self._add_qmod_qstruct(qmodule=QMODULE)

    def get_qmod_type(self) -> QuantumType:
        return TypeName(name=self._struct_name)

    @classmethod
    def to_qmod_quantum_type(cls, type_hint: Any) -> QuantumType:
        with _no_current_expandable():
            type_hint("DUMMY")
        return TypeName(name=type_hint.__name__)

    @classmethod
    def to_qvar(
        cls,
        origin: Union[str, HandleBinding],
        type_hint: Any,
        expr_str: Optional[str],
    ) -> "QStruct":
        field_types = {
            field_name: (QVar.from_type_hint(field_type), field_type)
            for field_name, field_type in type_hint.__annotations__.items()
        }
        illegal_fields = [
            (field_name, field_type)
            for field_name, (field_class, field_type) in field_types.items()
            if field_class is None
        ]
        if len(illegal_fields) > 0:
            raise ClassiqValueError(
                f"Field {illegal_fields[0][0]!r} of quantum struct "
                f"{type_hint.__name__} has a non-quantum type "
                f"{illegal_fields[0][1].__name__}."
            )
        base_handle = HandleBinding(name=origin) if isinstance(origin, str) else origin
        with _no_current_expandable():
            field_vars = {
                field_name: cast(Type[QVar], field_class).to_qvar(
                    FieldHandleBinding(base_handle=base_handle, field=field_name),
                    field_type,
                    f"get_field({expr_str if expr_str is not None else str(origin)}, '{field_name}')",
                )
                for field_name, (field_class, field_type) in field_types.items()
            }
        return QStruct(
            name=origin,
            _struct_name=type_hint.__name__,
            _fields=field_vars,
            _expr_str=expr_str,
        )

    def _add_qmod_qstruct(self, *, qmodule: ModelStateContainer) -> None:
        if self._struct_name in qmodule.qstruct_decls:
            return

        qmodule.qstruct_decls[self._struct_name] = QStructDeclaration(
            name=self._struct_name,
            fields={name: qvar.get_qmod_type() for name, qvar in self._fields.items()},
        )

    def _evaluate_size(self) -> int:
        return sum(var._evaluate_size() for var in self._fields.values())


def create_qvar_for_port_decl(port: AnonPortDeclaration, name: str) -> QVar:
    return _create_qvar_for_qtype(port.quantum_type, HandleBinding(name=name))


def _create_qvar_for_qtype(
    qtype: QuantumType, origin: HandleBinding, expr_str: Optional[str] = None
) -> QVar:
    # prevent addition to local handles, since this is used for ports
    with _no_current_expandable():
        if isinstance(qtype, QuantumBit):
            return QBit(origin, _expr_str=expr_str)
        elif isinstance(qtype, QuantumNumeric):
            return QNum(
                origin,
                qtype.size,
                qtype.is_signed,
                qtype.fraction_digits,
                _expr_str=expr_str,
            )
        elif isinstance(qtype, TypeName):
            struct_decl = QMODULE.qstruct_decls[qtype.name]
            return QStruct(
                origin,
                struct_decl.name,
                {
                    field_name: _create_qvar_for_qtype(
                        field_type,
                        FieldHandleBinding(base_handle=origin, field=field_name),
                        f"get_field({expr_str if expr_str is not None else str(origin)}, '{field_name}')",
                    )
                    for field_name, field_type in struct_decl.fields.items()
                },
                _expr_str=expr_str,
            )
        if TYPE_CHECKING:
            assert isinstance(qtype, QuantumBitvector)
        return QArray(origin, qtype.element_type, qtype.length, _expr_str=expr_str)


def get_qvar(qtype: QuantumType, origin: HandleBinding) -> "QVar":
    if isinstance(qtype, QuantumBit):
        return QBit(origin)
    elif isinstance(qtype, QuantumBitvector):
        return QArray(origin, qtype.element_type, qtype.length)
    elif isinstance(qtype, QuantumNumeric):
        return QNum(origin, qtype.size, qtype.is_signed, qtype.fraction_digits)
    elif isinstance(qtype, TypeName):
        return QStruct(
            origin,
            qtype.name,
            {
                field_name: get_qvar(
                    field_type, FieldHandleBinding(base_handle=origin, field=field_name)
                )
                for field_name, field_type in qtype.fields.items()
            },
        )
    raise NotImplementedError
