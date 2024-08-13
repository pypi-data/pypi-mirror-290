from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, Sequence, Union

import pydantic
from pydantic import Extra, Field

from classiq.interface.ast_node import ASTNode
from classiq.interface.generator.expressions.expression import Expression

HANDLE_ID_SEPARATOR = "___"


class HandleBinding(ASTNode):
    name: str = Field(default=None)

    class Config:
        frozen = True
        extra = Extra.forbid

    def __str__(self) -> str:
        return self.name

    def is_bindable(self) -> bool:
        return True

    @property
    def identifier(self) -> str:
        return self.name

    def collapse(self) -> "HandleBinding":
        return self

    def prefixes(self) -> Sequence["HandleBinding"]:
        """
        Split the handle into prefixes:
        a.b[0].c --> [a, a.b, a.b[0], a.b[0].c]
        """
        return [self]

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        return self.name == other_handle.name

    def overlaps(self, other_handle: "HandleBinding") -> bool:
        self_prefixes = self.collapse().prefixes()
        other_prefixes = other_handle.collapse().prefixes()
        return all(
            self_prefix._tail_overlaps(other_prefix)
            for self_prefix, other_prefix in zip(self_prefixes, other_prefixes)
        )


class NestedHandleBinding(HandleBinding):
    base_handle: "ConcreteHandleBinding"

    @pydantic.root_validator(pre=False)
    def _set_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "base_handle" in values:
            values["name"] = values["base_handle"].name
        return values

    def is_bindable(self) -> bool:
        return False

    def prefixes(self) -> Sequence["HandleBinding"]:
        return list(chain.from_iterable([self.base_handle.prefixes(), [self]]))


class SubscriptHandleBinding(NestedHandleBinding):
    index: Expression

    class Config:
        frozen = True
        extra = Extra.forbid

    def __str__(self) -> str:
        return f"{self.base_handle}[{self.index}]"

    @property
    def identifier(self) -> str:
        return f"{self.base_handle.identifier}{HANDLE_ID_SEPARATOR}{self.index}"

    def collapse(self) -> HandleBinding:
        if isinstance(self.base_handle, SlicedHandleBinding):
            return SubscriptHandleBinding(
                base_handle=self.base_handle.base_handle,
                index=self._get_collapsed_index(),
            ).collapse()
        return SubscriptHandleBinding(
            base_handle=self.base_handle.collapse(),
            index=self.index,
        )

    def _get_collapsed_index(self) -> Expression:
        if TYPE_CHECKING:
            assert isinstance(self.base_handle, SlicedHandleBinding)
        if self.index.is_evaluated() and self.base_handle.start.is_evaluated():
            return Expression(
                expr=str(
                    self.base_handle.start.to_int_value() + self.index.to_int_value()
                )
            )
        return Expression(expr=f"({self.base_handle.start})+({self.index})")

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        if isinstance(other_handle, SubscriptHandleBinding):
            return self.index == other_handle.index
        if (
            isinstance(other_handle, SlicedHandleBinding)
            and self.index.is_evaluated()
            and other_handle.start.is_evaluated()
            and other_handle.end.is_evaluated()
        ):
            return (
                other_handle.start.to_int_value()
                <= self.index.to_int_value()
                < other_handle.end.to_int_value()
            )
        return False


class SlicedHandleBinding(NestedHandleBinding):
    start: Expression
    end: Expression

    class Config:
        frozen = True
        extra = Extra.forbid

    def __str__(self) -> str:
        return f"{self.base_handle}[{self.start}:{self.end}]"

    @property
    def identifier(self) -> str:
        return (
            f"{self.base_handle.identifier}{HANDLE_ID_SEPARATOR}{self.start}_{self.end}"
        )

    def collapse(self) -> HandleBinding:
        if isinstance(self.base_handle, SlicedHandleBinding):
            return SubscriptHandleBinding(
                base_handle=self.base_handle.base_handle,
                start=self._get_collapsed_start(),
                end=self._get_collapsed_stop(),
            ).collapse()
        return SlicedHandleBinding(
            base_handle=self.base_handle.collapse(),
            start=self.start,
            end=self.end,
        )

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        if not self.start.is_evaluated() or not self.end.is_evaluated():
            return False
        start = self.start.to_int_value()
        end = self.end.to_int_value()
        if (
            isinstance(other_handle, SubscriptHandleBinding)
            and other_handle.index.is_evaluated()
        ):
            return start <= other_handle.index.to_int_value() < end
        if (
            isinstance(other_handle, SlicedHandleBinding)
            and other_handle.start.is_evaluated()
            and other_handle.end.is_evaluated()
        ):
            other_start = other_handle.start.to_int_value()
            other_end = other_handle.end.to_int_value()
            return start <= other_start < end or other_start <= start < other_end
        return False

    def _get_collapsed_start(self) -> Expression:
        if TYPE_CHECKING:
            assert isinstance(self.base_handle, SlicedHandleBinding)
        if self.start.is_evaluated() and self.base_handle.start.is_evaluated():
            return Expression(
                expr=str(
                    self.base_handle.start.to_int_value() + self.start.to_int_value()
                )
            )
        return Expression(expr=f"({self.base_handle.start})+({self.start})")

    def _get_collapsed_stop(self) -> Expression:
        if TYPE_CHECKING:
            assert isinstance(self.base_handle, SlicedHandleBinding)
        if self.end.is_evaluated() and self.base_handle.end.is_evaluated():
            return Expression(
                expr=str(self.base_handle.end.to_int_value() - self.end.to_int_value())
            )
        return Expression(expr=f"({self.base_handle.end})-({self.end})")


class FieldHandleBinding(NestedHandleBinding):
    field: str

    class Config:
        frozen = True
        extra = Extra.forbid

    def __str__(self) -> str:
        return f"{self.base_handle}.{self.field}"

    @property
    def identifier(self) -> str:
        return f"{self.base_handle.identifier}{HANDLE_ID_SEPARATOR}{self.field}"

    def collapse(self) -> HandleBinding:
        return FieldHandleBinding(
            base_handle=self.base_handle.collapse(),
            field=self.field,
        )

    def _tail_overlaps(self, other_handle: "HandleBinding") -> bool:
        return (
            isinstance(other_handle, FieldHandleBinding)
            and self.field == other_handle.field
        )


ConcreteHandleBinding = Union[
    HandleBinding,
    SubscriptHandleBinding,
    SlicedHandleBinding,
    FieldHandleBinding,
]
SubscriptHandleBinding.update_forward_refs(ConcreteHandleBinding=ConcreteHandleBinding)
SlicedHandleBinding.update_forward_refs(ConcreteHandleBinding=ConcreteHandleBinding)
FieldHandleBinding.update_forward_refs(ConcreteHandleBinding=ConcreteHandleBinding)
