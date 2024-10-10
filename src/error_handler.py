import sys
from token_type import TokenType
from token import Token


class ErrorHandler:
    has_error: bool = False

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
    def report(cls, line: int, where: str, message: str) -> None:
        sys.stderr.write(f"[line {line}] Error {where}: {message}\n")
        cls.has_error = True


class ParseError(RuntimeError):
    pass
