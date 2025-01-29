from tokens import Token
from error_handler import RuntimeErr


class Environment:
    def __init__(self, enclosing: "Environment | None" = None) -> None:
        self.enclosing: Environment | None = enclosing
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def ancestor(self, distance: int):
        env = self
        for _ in range(distance):
            if env.enclosing is None:
                break
            env = env.enclosing
        return env

    def get_at(self, distance: int, name: str):
        return self.ancestor(distance).values.get(name)

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeErr(f"undefined variable get'{name.lexeme}'.", token=name)

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeErr(f"Undefined variable assign'{name.lexeme}'.", token=name)

    def assign_at(self, distance: int, name: Token, val):
        self.ancestor(distance).values[name.lexeme] = val
