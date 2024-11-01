from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from tokens import Token

V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_binary_expression(self, expr: "Binary") -> V:
        ...

    @abstractmethod
    def visit_grouping_expression(self, expr: "Grouping") -> V:
        ...

    @abstractmethod
    def visit_literal_expression(self, expr: "Literal") -> V:
        ...

    @abstractmethod
    def visit_unary_expression(self, expr: "Unary") -> V:
        ...

    @abstractmethod
    def visit_variable_expression(self, expr: "Variable") -> V:
        ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[V]) -> V:
        ...


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expression(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expression(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expression(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expression(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name: Token = name

    def accept(self, visitor: Visitor):
        return visitor.visit_variable_expression(self)
