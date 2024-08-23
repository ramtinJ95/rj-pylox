import sys

from scanner import Scanner

# testing git commits package
class Lox:
    def __init__(self):
        self.had_error = False

    def run_file(self, path: str) -> None:
        file = open(path)
        self.run(file.read())
        if self.had_error:
            sys.exit(65)
        print("file")

    def run_prompt(self) -> None:
        while True:
            line = input("rj-plox> ")
            if line is None:
                break
            self.run(line)
            self.had_error = False
        print("prompt")

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

        print("run")

    @staticmethod
    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)

    @staticmethod
    def report(self, line: int, where: str, message: str) -> None:
        sys.stderr.write(f"[line {line}] Error {where}: {message}")


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: rjpylox [script name]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
