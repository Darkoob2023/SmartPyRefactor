import subprocess
import re
from .score_engine import compute_ast_score

def get_pylint_score(file_path):
    try:
        result = subprocess.run(
            ["pylint", file_path, "--score=y"],
            capture_output=True,
            text=True
        )
        output = result.stdout

        match = re.search(r"rated at (-?\d+\.\d+)/10", output)
        if match:
            raw_score = float(match.group(1))
        else:
            raw_score = 0.0 
    except Exception:
        raw_score = 0.0
    return raw_score


def get_combined_score(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        code_str = f.read()

    ast_score = compute_ast_score(code_str)

    pylint_score = get_pylint_score(file_path)

    combined = round(0.6 * pylint_score + 0.4 * ast_score, 1)

    return combined