import expr
from token_type import TokenType
from error_handler import RuntimeErr
from token import Token


class Interpreter(expr.Visitor):
    def __init__(self):
        pass

    def visit_literal_expression(self, expression: expr.Literal) -> object:
        return expression.value

    def visit_grouping_expression(self, expression: expr.Grouping) -> object:
        return self.evaluate(expression.expression)

    def visit_unary_expression(self, expression: expr.Unary) -> object:
        right = self.evaluate(expression.right)

        match expression.operator.type:
            case TokenType.MINUS:
                if isinstance(right, float):
                    return -(right)
                else:
                    print("oohh shit visit_unary_expression is fucked")
            case TokenType.BANG:
                return not self.is_truthy(right)
        return None

    def visit_binary_expression(self, expression: expr.Binary) -> object:
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)

        # these case matchings have to be done better with
        # isinstance checks later
        match expression.operator.type:
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
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
        if isinstance(obj, bool):
            return obj
        return True

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise RuntimeErr("Operand must be a number", token=operator)
