import sys


class Lox:
    def __main__(self):
        if len(sys.argv) > 2:
            print("Usage: rjpylox [script name]")
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

    def run_file(self, filename: str) -> None:
        print("file")

    def run_prompt(self):
        print("prompt")
