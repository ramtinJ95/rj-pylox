from enum import Enum
from typing import TYPE_CHECKING

from environment import Environment
from error_handler import Return
from lox_callable import LoxCallable

if TYPE_CHECKING:
    import interpreter
    import lox_instance
    import stmt

FunctionType = Enum("FunctionType", "NONE, FUNCTION, INITIALIZER, METHOD")


class LoxFunction(LoxCallable):
    def __init__(
        self,
        declaration: "stmt.Function",
        closure: Environment,
        is_init: bool = False,
    ) -> None:
        self.declaration = declaration
        self.closure = closure
        self.is_init = is_init

    def arity(self) -> int:
        return len(self.declaration.params)

    def bind(self, instance: "lox_instance.LoxInstance"):
        env = Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, self.is_init)

    def call(
        self, interpreter: "interpreter.Interpreter", args: list
    ) -> object:
        env = Environment(self.closure)
        for param, arg in zip(self.declaration.params, args):
            env.define(param.lexeme, arg)
        try:
            interpreter.execute_block(self.declaration.body, env)
        except Return as e:
            if self.is_init:
                return self.closure.get_at(0, "this")
            return e.val

        if self.is_init:
            return self.closure.get_at(0, "this")

        return None

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
