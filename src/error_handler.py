import sys


class ErrorHandler:
    has_error: bool = False

    @classmethod
    def error(cls, line: int, message: str) -> None:
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        sys.stderr.write(f"[line {line}] Error {where}: {message}")
        cls.has_error = True
