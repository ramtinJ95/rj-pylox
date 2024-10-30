import sys
from typing import TextIO

SPACE_4 = "    "
SPACE_8 = "        "


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    define_ast(
        output_dir,
        "Expr",
        [
            "Binary | left: Expr, operator: Token, right: Expr",
            "Grouping | expression: Expr",
            "Literal | value",
            "Unary | operator: Token, right: Expr",
        ],
        ["from token import Token"],
    )

    define_ast(output_dir, "Stmt",
               [
                   "Expression | expression: Expr",
                   "Print | expression: Expr"
               ],
               ["from expr import Expr"]
               )


def define_ast(
    output_dir: str, base_name: str, types: list[str], extra_imports: list[str] = None
) -> None:
    lower_base_name = base_name.lower()
    path = output_dir + "/" + lower_base_name + ".py"
    output_writer = open(path, "w", encoding="UTF-8")

    define_imports(output_writer, extra_imports)
    define_visitor(output_writer, base_name, types)
    define_base_class(output_writer, base_name)

    for type in types:
        class_name = type.split("|", 1)[0].strip()
        fields = type.split("|", 1)[1].strip()
        define_type(output_writer, base_name, class_name, fields)


def define_type(output_writer: TextIO, base_name: str, class_name: str, fields: str) -> None:
    output_writer.write("\n\n")
    output_writer.write(f"class {class_name}({base_name}):\n")
    # Follow 80 char limit
    if len(fields) < 55:
        output_writer.write(f"    def __init__(self, {fields}):\n")
    elif len(fields) < 65:
        output_writer.write("    def __init__(\n")
        output_writer.write("        self, " + fields)
        output_writer.write("\n    ):\n")
    else:
        output_writer.write("    def __init__(\n        ")
        output_writer.write(",\n        ".join(["self"] + fields.split(", ")))
        output_writer.write(",\n    ):\n")

    fields_list = fields.split(", ")
    for field in fields_list:
        name = field.strip()
        output_writer.write(f"{SPACE_8}self.{name} = {name.split(':')[0]}\n")
    output_writer.write("\n")

    output_writer.write(f"{SPACE_4}def accept(self, visitor: Visitor):\n")
    output_writer.write(
        f"{SPACE_8}return visitor.visit_" f"{class_name.lower()}_{base_name.lower()}(self)\n"
    )


def define_visitor(output_writer: TextIO, base_name: str, types: list[str]) -> None:
    output_writer.write('V = TypeVar("V")\n\n\n')
    output_writer.write("class Visitor(ABC, Generic[V]):\n")

    for type in types:
        type_name = type.split("|")[0].strip()
        output_writer.write(f"{SPACE_4}@abstractmethod\n")
        output_writer.write(
            f"{SPACE_4}def visit_{type_name.lower()}_{base_name.lower()}"
            f'(self, {base_name.lower()}: "{type_name}") -> V:\n'
        )
        output_writer.write(f"{SPACE_8}...\n\n")

    output_writer.write("\n")


def define_imports(output_writer: TextIO, extra_imports: list[str] = None) -> None:
    output_writer.write("from abc import ABC, abstractmethod\n")
    output_writer.write("from typing import Generic, TypeVar\n\n")
    for imprt in extra_imports:
        output_writer.write(imprt + "\n")
    output_writer.write("\n")


def define_base_class(output_writer: TextIO, base_name: str) -> None:
    output_writer.write(f"class {base_name}(ABC):\n")
    output_writer.write(f"{SPACE_4}@abstractmethod\n")
    output_writer.write(
        f"{SPACE_4}def accept(self, visitor: Visitor[V]) -> V:\n")
    output_writer.write(f"{SPACE_8}...\n")


if __name__ == "__main__":
    main()
