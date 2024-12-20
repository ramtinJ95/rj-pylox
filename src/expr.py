from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from token import Token

V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_assign_expression(self, expression: "Assign") -> V:
        ...

    @abstractmethod
    def visit_binary_expression(self, expression: "Binary") -> V:
        ...

    @abstractmethod
    def visit_call_expression(self, expression: "Call") -> V:
        ...

    @abstractmethod
    def visit_grouping_expression(self, expression: "Grouping") -> V:
        ...

    @abstractmethod
    def visit_literal_expression(self, expression: "Literal") -> V:
        ...

    @abstractmethod
    def visit_logical_expression(self, expression: "Logical") -> V:
        ...

    @abstractmethod
    def visit_unary_expression(self, expression: "Unary") -> V:
        ...

    @abstractmethod
    def visit_variable_expression(self, expression: "Variable") -> V:
        ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[V]) -> V:
        ...


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor: Visitor):
        return visitor.visit_assign_expression(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expression(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, args: list[Expr]):
        self.callee: Expr = callee
        self.paren: Token = paren
        self.args: list[Expr] = args

    def accept(self, visitor: Visitor):
        return visitor.visit_call_expression(self)


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


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_logical_expression(self)


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
