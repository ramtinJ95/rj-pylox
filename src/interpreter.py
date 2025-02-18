import expr
import stmt
import time
from token_type import TokenType
from lox_callable import LoxCallable
from lox_function import LoxFunction
from error_handler import ErrorHandler, RuntimeErr, Return
from tokens import Token
from environment import Environment

# TODO: change all these return and parameter types that are object to a
# smaller subset like int | float etc

# TODO: Remove this clock class and build proper STD for Lox


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", args: list) -> float:
        return time.time()

    def __str__(self) -> str:
        return "<native clock function>"


class Interpreter(expr.Visitor, stmt.Visitor):
    global_env = Environment()

    def __init__(self):
        self.env = self.global_env
        self.locals: dict[expr.Expr, int] = {}

    def interpret(self, statements: list[stmt.Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeErr as error:
            ErrorHandler.runtime_error(error)

    def resolve(self, expr: expr.Expr, depth: int):
        self.locals[expr] = depth

    def visit_literal_expression(self, expression: expr.Literal) -> object:
        return expression.value

    def visit_logical_expression(self, expression: expr.Logical) -> object:
        left = self.evaluate(expression.left)

        if expression.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
            return self.evaluate(expression.right)
        if expression.operator.type == TokenType.AND:
            if not self.is_truthy(left):
                return left
            return self.evaluate(expression.right)

    def visit_grouping_expression(self, expression: expr.Grouping) -> object:
        return self.evaluate(expression.expression)

    def visit_unary_expression(self, expression: expr.Unary) -> object:
        right = self.evaluate(expression.right)

        match expression.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expression.operator, right)
                return -(right)
            case TokenType.BANG:
                return not self.is_truthy(right)
        return None

    def visit_variable_expression(self, expression: expr.Variable) -> object:
        return self.lookup_variable(expression.name, expression)

    def lookup_variable(self, name, expression: expr.Expr) -> object:
        distance = self.locals.get(expression)
        if distance is not None:
            return self.env.get_at(distance, name.lexeme)
        else:
            return self.global_env.get(name)

    def visit_binary_expression(self, expression: expr.Binary) -> object:
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)

        # these case matchings have to be done better with
        # isinstance checks later
        match expression.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expression.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise RuntimeErr(
                    "Operands must be two numbers or two strings.", token=expression.operator)
            case TokenType.SLASH:
                self.check_number_operands(expression.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expression.operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self.check_number_operands(expression.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expression.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expression.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expression.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right

        return None

    def visit_call_expression(self, expression: expr.Call) -> object:
        callee = self.evaluate(expression.callee)
        arguments = [self.evaluate(arg) for arg in expression.args]
        if len(arguments) != callee.arity():
            raise RuntimeErr(
                f"Expected {callee.arity()} arguments got {len(arguments)}.",
                token=expression.paren
            )
        try:
            return callee.call(self, arguments)
        except Exception as e:
            raise RuntimeErr(e.args[0] ,token=expression.paren)

    def evaluate(self, expression: expr.Expr) -> object:
        return expression.accept(self)

    def execute(self, statement: stmt.Stmt) -> None:
        statement.accept(self)

    def execute_block(self, statments: list[stmt.Stmt], environment: Environment) -> None:
        previous = self.env
        try:
            self.env = environment
            for statement in statments:
                self.execute(statement)
        finally:
            self.env = previous

    def visit_block_stmt(self, statement: stmt.Block) -> None:
        self.execute_block(statement.statements, Environment(self.env))

    # I dont think this is necessary in python, this evaluate step is probably
    # a java only thing
    def visit_expression_stmt(self, statement: stmt.Expression) -> None:
        self.evaluate(statement.expression)
        return None

    def visit_function_stmt(self, statement: stmt.Function) -> None:
        function = LoxFunction(statement, self.env)
        self.env.define(statement.name.lexeme, function)
        return None

    def visit_if_stmt(self, statement: stmt.If) -> None:
        if self.is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.then_branch)

        elif statement.else_branch is not None:
            self.execute(statement.else_branch)

        return None

    def visit_print_stmt(self, statement: stmt.Print) -> None:
        value = self.evaluate(statement.expression)
        print(self.stringify(value))
        return None

    def visit_return_stmt(self, statement: stmt.Return) -> None:
        value = None
        if statement.value is not None:
            value = self.evaluate(statement.value)
        raise Return(value)

    def visit_var_stmt(self, statement: stmt.Var) -> None:
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)
        self.env.define(statement.name.lexeme, value)
        return None

    def visit_while_stmt(self, statement: stmt.While) -> None:
        while self.is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.body)

        return None

    def visit_assign_expression(self, expression: expr.Assign) -> object:
        value = self.evaluate(expression.value)
        distance = self.locals.get(expression)
        if distance is not None:
            self.env.assign_at(distance, expression.name, value)
        else:
            self.global_env.assign(expression.name, value)

        return value

    def is_truthy(self, obj: object) -> bool:
        return obj is not None and obj is not False

    def stringify(self, obj: object) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float) and isinstance(obj, int):
            return str(int(obj))
        return str(obj)

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise RuntimeErr("Operand must be a number", token=operator)

    def check_number_operands(self, operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeErr("Operands must be numbers.", token=operator)
