from __future__ import annotations
import ast
import enum
import inspect

class gAAAAABmuzW5EexpoV_KtWeJkKpWQgu1cphjMjhiKCK3K5NXF8x6awwVOIXVLwOICI5gvz3IZzM80qMyLRRmIRnnzBwM3n7Vhg__(ast.NodeVisitor):

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

def gAAAAABmuzW5dXTy2i0GXSsxvau8coj_KU__n1Fc0YFdys4CEsRpgPeZ0rGjew8f_aQPfM_SiRMHVbnmTzl4W8DEcoapOpYrJg__(enum_class: type[enum.Enum]) -> list[tuple[str, str, str]]:
    source = inspect.getsource(enum_class)
    ast_tree = getattr(ast, 'parse')(source)
    visitor = gAAAAABmuzW5EexpoV_KtWeJkKpWQgu1cphjMjhiKCK3K5NXF8x6awwVOIXVLwOICI5gvz3IZzM80qMyLRRmIRnnzBwM3n7Vhg__()
    visitor.visit(ast_tree)
    return visitor.fields