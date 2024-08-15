from typing import Any

type SQLAlchemyTable = Any

from .clauses import BooleanClause
from .visitor import BaseVisitor


class SQLAlchemyVisitor(BaseVisitor):
    def visit_eq(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field) == comparison.value

    def visit_ne(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field) != comparison.value

    def visit_lt(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field) < comparison.value

    def visit_le(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field) <= comparison.value

    def visit_gt(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field) > comparison.value

    def visit_ge(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field) >= comparison.value

    def visit_in(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field).in_(comparison.value)

    def visit_like(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        return self._attr(_object_mapping, comparison.field).ilike(
            comparison.value, escape="\\"
        )

    def visit_not_like(
        self, _object_mapping: dict[Any, Any], comparison: BooleanClause
    ):
        return self._attr(_object_mapping, comparison.field).not_ilike(
            comparison.value, escape="\\"
        )

    def visit_or(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        _op = comparisons[0]
        for comp in comparisons[1:]:
            _op = _op | comp  #! <--- Caution: do not modify bitwise operator

        return _op

    def visit_and(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        _op = comparisons[0]
        for comp in comparisons[1:]:
            _op = _op & comp  #! <--- Caution: do not modify bitwise operator
        return _op

    def visit_xor(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        return (
            comparisons[0] ^ comparisons[1]
        )  #! <--- Caution: do not modify bitwise operator

    def visit_not(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        return ~comparisons[0]  #! <--- Caution: do not modify bitwise operator
