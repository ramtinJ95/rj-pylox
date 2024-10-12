import expr
from token_type import TokenType
from error_handler import ErrorHandler, RuntimeErr
from token import Token


class Interpreter(expr.Visitor):
    def __init__(self):
        pass

    def interpret(self, expression: expr.Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(f"This is the value: {value}")
            print(self.stringify(value))
        except RuntimeErr as error:
            ErrorHandler.runtime_error(error)

    def visit_literal_expression(self, expression: expr.Literal) -> object:
        print(f"We in visit_literal: {expression.__str__()}")
        return expression.value

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

    def visit_binary_expression(self, expression: expr.Binary) -> object:
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        print("kamel")

        # these case matchings have to be done better with
        # isinstance checks later
        match expression.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expression.operator, left, right)
                print("we in the TokenType.MINUS thingy")
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise RuntimeErr(
                    "Operands must be two numbers or two strings.", expression.operator)
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

    def evaluate(self, expression: expr.Expr) -> object:
        return expression.accept(self)

    def is_truthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, float):
            return obj.__str__()
        return True

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
            print("we in check_number_operands")
            return
        raise RuntimeErr("Operands must be numbers.", token=operator)
