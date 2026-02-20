import ast

def compute_ast_score(code_str):
    tree = ast.parse(code_str)
    for_count = sum(isinstance(n, ast.For) for n in ast.walk(tree))
    while_count = sum(isinstance(n, ast.While) for n in ast.walk(tree))
    func_count = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))

    score = 10 - 0.5*for_count - 0.5*while_count - 0.2*func_count
    if score < 0:
        score = 0
    return round(score, 1)