import sys
from typing import TextIO

SPACE_4 = "    "
SPACE_8 = "        "


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
        "Binary | left, operator, right",
        "Grouping | expression",
        "Literal | value",
        "Unary | operator, right",
    ])


def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    path = output_dir + "/" + base_name + ".py"
    output_writer = open(path, "w", encoding="UTF-8")

    output_writer.write("from abc import ABC, abstractmethod\n")
    output_writer.write("from token import *\n")
    output_writer.write("\n")

    output_writer.write(f"class {base_name}:\n")
    output_writer.write(f"{SPACE_4}pass\n")

    for type in types:
        class_name = type.split("|")[0].strip()
        fields = type.split("|")[1].strip()
        define_type(output_writer, base_name, class_name, fields)


def define_type(
        output_writer: TextIO, base_name: str, class_name: str, fields: str) -> None:
    output_writer.write(f"\nclass {class_name}({base_name}):\n")
    output_writer.write(f"{SPACE_4}def __init__(self, {fields}):\n")

    fields_list = fields.split(", ")
    for field in fields_list:
        name = field.strip()
        output_writer.write(f"{SPACE_8}self.{name} = {name}\n")
    output_writer.write("\n")


if __name__ == "__main__":
    main()
