import ast

class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.for_count = 0
        self.while_count = 0
        self.if_count = 0
        self.function_count = 0
        self.max_depth = 0
        self.current_depth = 0

    def visit_For(self, node):
        self.for_count += 1
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_While(self, node):
        self.while_count += 1
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_If(self, node):
        self.if_count += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)

def analyze_code(code_str):
    tree = ast.parse(code_str)
    analyzer = ASTAnalyzer()
    analyzer.visit(tree)
    return {
        "for_loops": analyzer.for_count,
        "while_loops": analyzer.while_count,
        "if_statements": analyzer.if_count,
        "functions": analyzer.function_count,
        "max_nesting_depth": analyzer.max_depth
    }