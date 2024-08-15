import abc
from typing import Any

from .clauses import BooleanClause, BooleanClauseList
from .filter import Attribute, Filter


class BaseVisitor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "visit_eq")
            and callable(subclass.visit_eq)
            and hasattr(subclass, "visit_ne")
            and callable(subclass.visit_ne)
            and hasattr(subclass, "visit_lt")
            and callable(subclass.visit_lt)
            and hasattr(subclass, "visit_le")
            and callable(subclass.visit_le)
            and hasattr(subclass, "visit_gt")
            and callable(subclass.visit_gt)
            and hasattr(subclass, "visit_ge")
            and callable(subclass.visit_ge)
            and hasattr(subclass, "visit_in")
            and callable(subclass.visit_in)
            and hasattr(subclass, "visit_like")
            and callable(subclass.visit_like)
            and hasattr(subclass, "visit_not_like")
            and callable(subclass.visit_not_like)
            and hasattr(subclass, "visit_or")
            and callable(subclass.visit_or)
            and hasattr(subclass, "visit_and")
            and callable(subclass.visit_and)
            and hasattr(subclass, "visit_xor")
            and callable(subclass.visit_xor)
            and hasattr(subclass, "visit_not")
            and callable(subclass.visit_not)
            or NotImplemented
        )

    def _attr(self, _object_mapping: dict[Any, Any], field: Attribute):
        _object = _object_mapping.get(field.parent_class)
        if _object is None:
            raise RuntimeError(
                f"Invalid _object_mapping. Missing class '{field.parent_class.__name__}'."
            )

        if not hasattr(_object, field.name):
            raise ValueError(
                f"'{field.name}' is not a valid attribute of '{field.parent_class.__name__}'"
            )

        return getattr(_object, field.name)

    def visit(
        self,
        _object_mapping: dict[Any, Any],
        _filter: Filter,
    ):
        if not isinstance(_filter, Filter):
            raise ValueError("_filter argument should be an instance of Filter.")

        clause = _filter.clause
        if clause is None:
            return None

        name = clause.__class__.__name__.lower()
        method = getattr(self, "visit_" + name)

        if isinstance(clause, BooleanClauseList):
            comparisons = []
            for item in clause.clause_list:
                comparisons.append(self.visit(_object_mapping, Filter(item)))

            return method(_object_mapping, comparisons)

        return method(_object_mapping, clause)

    @abc.abstractmethod
    def visit_eq(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_ne(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_lt(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_le(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_gt(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_ge(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_in(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_like(self, _object_mapping: dict[Any, Any], comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_not_like(
        self, _object_mapping: dict[Any, Any], comparison: BooleanClause
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_or(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_and(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_xor(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_not(self, _object_mapping: dict[Any, Any], comparisons: list[Any]):
        raise NotImplementedError
