from __future__ import annotations
import ast
import enum
import inspect

class gAAAAABmvnuP02y1GV3Vvl3JKflY7J0uQd91GXousiVW_5DXTDU3_ARbWKvDG2FIvgvQQrZJDqemqoabY9Hw6c1UUeOuEUXsuQ__(ast.NodeVisitor):

    def __init__(self) -> None:
        self.parents: list[ast.AST] = []
        self.fields: list[tuple[str, str, str]] = []

    def generic_visit(self, node: ast.AST) -> None:
        self.parents.append(node)
        super().generic_visit(node)
        self.parents.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        assert len(node.targets) == 1
        assert isinstance(node.targets[0], ast.Name)
        assert isinstance(node.value, ast.Constant)
        value = node.value.value
        siblings = list(ast.iter_child_nodes(self.parents[-1]))
        docstring_node = siblings[siblings.index(node) + 1]
        assert isinstance(docstring_node, ast.Expr) and isinstance(docstring_node.value, ast.Constant)
        docstring = docstring_node.value.value
        self.fields.append((node.targets[0].id, value, docstring))

def gAAAAABmvnuPh_RfeQQpTnK1h4nq6S_bEm2siG9it9hR9TQI_oX5EtL_wTalS4YK7yxXUF0LWBEojJkcZXUlG4Q4ktA_wBUHww__(enum_class: type[enum.Enum]) -> list[tuple[str, str, str]]:
    source = inspect.getsource(enum_class)
    ast_tree = getattr(ast, 'parse')(source)
    visitor = gAAAAABmvnuP02y1GV3Vvl3JKflY7J0uQd91GXousiVW_5DXTDU3_ARbWKvDG2FIvgvQQrZJDqemqoabY9Hw6c1UUeOuEUXsuQ__()
    visitor.visit(ast_tree)
    return visitor.fields