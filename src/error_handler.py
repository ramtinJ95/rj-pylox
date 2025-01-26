import sys
from tokens import Token

from token_type import TokenType


class ParseError(RuntimeError):
    pass


class Return(RuntimeError):
    def __init__(self, value) -> None:
        self.value = value


class RuntimeErr(RuntimeError):
    def __init__(self, *args: object, token: Token) -> None:
        super().__init__(*args)
        self.token = token


class ErrorHandler:
    has_error: bool = False
    had_runtime_error: bool = False

    @classmethod
    def error(cls, where: int | Token, message: str) -> None:
        if isinstance(where, Token):
            if where.type == TokenType.EOF:
                cls.report(where.line, " at end", message)
            else:
                cls.report(where.line, f" at '{where.lexeme}'", message)
        else:
            cls.report(where, "", message)

    @classmethod
    def runtime_error(cls, error: RuntimeErr):
        print(f"[line {error.token.line}]: {error.args[0]}")
        cls.had_runtime_error = True

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        sys.stderr.write(f"[line {line}] Error {where}: {message}\n")
        cls.has_error = True
