import itertools
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

import pyomo.environ as pyo
from pyomo.core.base import _GeneralVarData
from pyomo.core.expr.visitor import clone_expression, identify_variables

from classiq.interface.combinatorial_optimization.encoding_types import EncodingType
from classiq.interface.exceptions import ClassiqCombOptError

from classiq.applications.combinatorial_helpers import pyomo_utils


@dataclass
class VarExpressionMapping:
    var: _GeneralVarData
    expr: pyo.Expression
    encodings_vars: List[_GeneralVarData] = field(default_factory=list)


class EncodingMapping:
    def __init__(self, encoding_type: EncodingType) -> None:
        self._data: List[VarExpressionMapping] = []
        self.encoding_type = encoding_type

    @property
    def original_vars(self) -> List[_GeneralVarData]:
        return [pair.var for pair in self._data]

    @property
    def encodings_vars(self) -> List[_GeneralVarData]:
        return list(
            itertools.chain.from_iterable(
                var_mapping.encodings_vars for var_mapping in self._data
            )
        )

    @property
    def substitution_dict(self) -> Dict[int, pyo.Expression]:
        return {id(mapping.var): mapping.expr for mapping in self._data}

    def __len__(self) -> int:
        return len(self._data)

    def add(
        self,
        original_var: _GeneralVarData,
        encoding_expr: pyo.Expression,
        encodings_vars: Union[List[_GeneralVarData], None] = None,
    ) -> None:
        if encodings_vars is None:
            encodings_vars = list(identify_variables(encoding_expr))

        self._check_unique_encoding_vars(encodings_vars)
        self._data.append(
            VarExpressionMapping(
                var=original_var, expr=encoding_expr, encodings_vars=encodings_vars
            )
        )

    def _check_unique_encoding_vars(self, variables: List[_GeneralVarData]) -> None:
        assert all(
            not pyomo_utils.contains(var, self.encodings_vars) for var in variables
        )

    def get_var_expr_mapping(
        self, original_var: _GeneralVarData
    ) -> VarExpressionMapping:
        for var_expr_mapping in self._data:
            if var_expr_mapping.var is original_var:
                return var_expr_mapping
        raise ClassiqCombOptError("No variable expression mapping found.")

    def get_encoding_vars(self, original_var: _GeneralVarData) -> List[_GeneralVarData]:
        return self.get_var_expr_mapping(original_var).encodings_vars

    def get_original_var(
        self, encoding_var: _GeneralVarData
    ) -> Optional[_GeneralVarData]:
        for original_var in self.original_vars:
            if pyomo_utils.contains(encoding_var, self.get_encoding_vars(original_var)):
                return original_var
        return None

    def decode(self, solution: List[int]) -> List[int]:
        idx = 0
        decoded_solution = []
        for var_mapping in self._data:
            num_encoding_vars = len(var_mapping.encodings_vars)
            encoding_vars_solution = solution[idx : idx + num_encoding_vars]
            idx += num_encoding_vars

            substitution_map = {
                id(var): num
                for var, num in zip(var_mapping.encodings_vars, encoding_vars_solution)
            }
            substituted_expr = clone_expression(
                var_mapping.expr, substitute=substitution_map
            )

            if callable(substituted_expr):
                substituted_expr = substituted_expr()

            decoded_solution.append(substituted_expr)

        return decoded_solution
