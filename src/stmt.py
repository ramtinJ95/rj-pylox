from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from expr import Expr

V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression") -> V:
        ...

    @abstractmethod
    def visit_print_stmt(self, stmt: "Print") -> V:
        ...


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[V]) -> V:
        ...


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)
