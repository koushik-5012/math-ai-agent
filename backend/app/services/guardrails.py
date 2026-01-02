import re

def check_math_guardrails(question: str) -> bool:
    """
    Returns True ONLY if the question is clearly math-related.
    Strict but practical guardrails.
    """

    q = question.lower().strip()

    # -----------------------------
    # 1️⃣ HARD BLOCK: known non-math topics
    # -----------------------------
    non_math_patterns = [
        r"\bgoogle\b",
        r"\bceo\b",
        r"\bpresident\b",
        r"\bmovie\b",
        r"\bactor\b",
        r"\bweather\b",
        r"\bnews\b",
        r"\bcapital\b",
        r"\bcountry\b",
    ]

    for pat in non_math_patterns:
        if re.search(pat, q):
            return False

    # -----------------------------
    # 2️⃣ Keyword-based math intent
    # -----------------------------
    math_keywords = [
        "solve", "equation", "factor", "expand", "simplify",
        "derivative", "differentiate", "integral", "limit",
        "sin", "cos", "tan", "cot", "sec", "cosec",
        "matrix", "vector", "eigenvalue", "eigenvector",
        "lcm", "hcf", "gcd", "multiple", "divisor", "remainder",
        "probability", "mean", "median", "variance",
        "theorem", "prove", "proof",
        "function", "graph"
    ]

    for keyword in math_keywords:
        if re.search(rf"\b{keyword}\b", q):
            return True

    # -----------------------------
    # 3️⃣ Math expression detection
    # -----------------------------
    expression_pattern = r"""
        (
            [0-9]+\s*[\+\-\*/^=]\s*[0-9]+ |
            [a-z]\s*\^\s*[0-9]+ |
            sin\s*\(|cos\s*\(|tan\s*\(|ln\s*\(
        )
    """

    if re.search(expression_pattern, q, re.VERBOSE):
        return True

    # -----------------------------
    # 4️⃣ Numbers + math intent
    # -----------------------------
    contains_numbers = re.search(r"\d+", q)
    contains_math_word = re.search(r"\b(lcm|hcf|gcd|multiple|divisor|remainder)\b", q)

    if contains_numbers and contains_math_word:
        return True

    # -----------------------------
    # 5️⃣ Final decision
    # -----------------------------
    return False
