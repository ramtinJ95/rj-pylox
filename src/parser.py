import expr
from token import Token
from token_type import TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current = 0
        self.tokens = tokens

    def expressions(self) -> expr.Expr:
        return self.equality()

    def equality(self) -> expr.Expr:
        expression = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = expr.Binary(expression, operator, right)

        return expression
