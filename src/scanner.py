from token import Token
from typing import Dict

from token_type import TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords: Dict[str, TokenType] = {
            "add": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        char = self.advance()
        if char == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self.add_token(TokenType.COMMA)
        elif char == ".":
            self.add_token(TokenType.DOT)
        elif char == "-":
            self.add_token(TokenType.MINUS)
        elif char == "+":
            self.add_token(TokenType.PLUS)
        elif char == ";":
            self.add_token(TokenType.SEMICOLON)
        elif char == "*":
            self.add_token(TokenType.STAR)
        elif char == "!":
            self.add_token(TokenType.BANG_EQUAL) if self.match(
                "=") else self.add_token(TokenType.BANG)
        elif char == "=":
            self.add_token(TokenType.EQUAL_EQUAL) if self.match(
                "=") else self.add_token(TokenType.EQUAL)
        elif char == "<":
            self.add_token(TokenType.LESS_EQUAL) if self.match(
                "=") else self.add_token(TokenType.LESS)
        elif char == ">":
            self.add_token(TokenType.GREATER_EQUAL) if self.match(
                "=") else self.add_token(TokenType.GREATER)
        elif char == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end:
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif char == " ":
            pass
        elif char == "\r":
            pass
        elif char == "\t":
            pass
        elif char == "\n":
            self.line += 1
        elif char == '"':
            self._string()

        else:
            if char.isdigit():
                self._number()
            elif char.isalpha():
                self.identifier()

            else:
                print(f"{self.line}, Unexpected character")

    def _string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            print(f"{self.line}, Unterminated string")
            return

        self.advance()

        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(
            self.source[self.start: self.current]))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: object = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start: self.current]
        _type = self.keywords.get(text)
        if _type is None:
            _type = TokenType.IDENTIFIER

        self.add_token(_type)

    def is_alpha_numeric(self, char: str) -> bool:
        return char.isalpha() or char.isdigit()
