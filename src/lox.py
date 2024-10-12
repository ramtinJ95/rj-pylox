import sys
from parser import Parser

from error_handler import ErrorHandler
from scanner import Scanner
from interpreter import Interpreter


class Lox:
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter

    def run_file(self, path: str) -> None:
        file = open(path)
        self.run(file.read())
        if ErrorHandler.has_error:
            sys.exit(65)
        if ErrorHandler.had_runtime_error:
            sys.exit(70)

    def run_prompt(self) -> None:
        while True:
            line = input("rj-plox> ")
            if line is None or line == "exit()":
                break
            self.run(line)
            ErrorHandler.has_error = False

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        print(expression)
        if ErrorHandler.has_error:
            sys.exit(65)
        if ErrorHandler.had_runtime_error:
            sys.exit(70)
        self.interpreter.interpret(expression)


if __name__ == "__main__":
    interpreter = Interpreter()
    # this whole thing irks me will fix later
    # need it to use the same interpreter instance
    lox = Lox(interpreter)
    if len(sys.argv) > 2:
        print("Usage: rjpylox [script name]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
