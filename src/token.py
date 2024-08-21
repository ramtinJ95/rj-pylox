from token_type import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return (
            f'Token<{self.type.name}{": " + str(self.lexeme) if self.lexeme else ""}, {self.line}>'
        )

    def __repr__(self):
        return self.__str__()
