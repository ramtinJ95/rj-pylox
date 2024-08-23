from token import Token

from token_type import TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        char = self.advance()
        if char == "(":
            self.add_token(TokenType.LEFT_PARAM)
        if char == ")":
            self.add_token(TokenType.RIGHT_PARAM)

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:

