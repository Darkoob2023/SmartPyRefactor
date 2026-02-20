import ast
import difflib

class AdvancedRefactor(ast.NodeTransformer):

    def __init__(self):
        self.warnings = []
        self.set_suggestions = []

    def visit_For(self, node):
        if hasattr(node, 'parent') and isinstance(node.parent, ast.For):
            self.warnings.append(f"Nested loop at line {node.lineno}")

        if (
            len(node.body) == 1
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Call)
        ):
            call = node.body[0].value
            if (
                isinstance(call.func, ast.Attribute)
                and call.func.attr == "append"
                and len(call.args) == 1
            ):
                list_name = call.func.value.id
                element = call.args[0]
                self.set_suggestions.append(
                    f"Consider using set() for {list_name} at line {node.lineno}"
                )
                list_comp = ast.ListComp(
                    elt=element,
                    generators=[
                        ast.comprehension(
                            target=node.target,
                            iter=node.iter,
                            ifs=[],
                            is_async=0
                        )
                    ]
                )
                return ast.Assign(
                    targets=[ast.Name(id=list_name, ctx=ast.Store())],
                    value=list_comp
                )

        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        start = node.lineno
        end = max((getattr(n, 'lineno', start) for n in ast.walk(node)), default=start)
        length = end - start + 1
        if length > 15:
            self.warnings.append(f"Long function '{node.name}' ({length} lines)")
        return self.generic_visit(node)

def set_parents(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

def refactor_code(code_str):
    try:
        tree = ast.parse(code_str)
        set_parents(tree)
        transformer = AdvancedRefactor()
        new_tree = transformer.visit(tree)
        ast.fix_missing_locations(new_tree)
        refactored_code = ast.unparse(new_tree)

        diff = list(difflib.unified_diff(
            code_str.splitlines(),
            refactored_code.splitlines(),
            lineterm=""
        ))

        diff_text = "\n".join(diff)
        warnings = transformer.warnings + transformer.set_suggestions
        return refactored_code, warnings, diff_text
    except Exception:
        return code_str, [], ""