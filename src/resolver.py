from typing import TYPE_CHECKING

import expr as ex
import stmt as st
from error_handler import ErrorHandler
from lox_function import FunctionType

if TYPE_CHECKING:
    import interpreter
    from tokens import Token


class Resolver(ex.Visitor, st.Visitor):
    def __init__(self, interpreter: "interpreter.Interpreter") -> None:
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE

    def resolve_expr(self, expr: ex.Expr):
        return expr.accept(self)

    def resolve_function(self, stmt: st.Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in stmt.params:
            self.declare(param)
            self.define(param)
        self.resolve_stmts(stmt.body)
        self.end_scope()
        self.current_function = enclosing_function

    def resolve_local(self, expr: ex.Expr, name: "Token"):
        for i in range(len(self.scopes)):
            if name.lexeme in self.scopes[~i]:
                self.interpreter.resolve(expr, i)
                return

    def resolve_stmt(self, stmt: st.Stmt):
        stmt.accept(self)

    def resolve_stmts(self, stmts: list[st.Stmt]):
        for stmt in stmts:
            self.resolve_stmt(stmt)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: "Token"):
        if not self.scopes:
            return

        scope = self.scopes[-1]
        if name.lexeme in scope:
            ErrorHandler.error(
                name, "Already a variable with this name in this scope."
            )

        scope[name.lexeme] = False

    def define(self, name: "Token"):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def visit_block_stmt(self, stmt: st.Block):
        self.begin_scope()
        self.resolve_stmts(stmt.statements)
        self.end_scope()

    def visit_expression_stmt(self, stmt: st.Expression):
        self.resolve_expr(stmt.expression)

    def visit_function_stmt(self, stmt: st.Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: st.If):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_stmt(stmt.else_branch)

    def visit_print_stmt(self, stmt: st.Print):
        self.resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt: st.Return):
        if self.current_function == FunctionType.NONE:
            ErrorHandler.error(
                stmt.keyword, "Can't return from top-level code."
            )

        if (
            self.current_function == FunctionType.INITIALIZER
            and stmt.value is not None
        ):
            ErrorHandler.error(
                stmt.keyword, "Can't return a value from an initializer."
            )

        if stmt.value is not None:
            self.resolve_expr(stmt.value)

    def visit_var_stmt(self, stmt: st.Var):
        self.declare(stmt.name)

        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)

        self.define(stmt.name)

    def visit_while_stmt(self, stmt: st.While):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_assign_expression(self, expr: ex.Assign):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expression(self, expr: ex.Binary):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call_expression(self, expr: ex.Call):
        self.resolve_expr(expr.callee)
        for arg in expr.args:
            self.resolve_expr(arg)

    def visit_grouping_expression(self, expr: ex.Grouping):
        self.resolve_expr(expr.expression)

    def visit_literal_expression(self, expr: ex.Literal):
        pass

    def visit_logical_expression(self, expr: ex.Logical):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_unary_expression(self, expr: ex.Unary):
        self.resolve_expr(expr.right)

    def visit_variable_expression(self, expr: ex.Variable):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            ErrorHandler.error(
                expr.name, "Can't read local variable in its own initializer."
            )

        self.resolve_local(expr, expr.name)
