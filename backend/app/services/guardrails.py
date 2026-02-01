import re

def check_math_guardrails(question: str) -> bool:
    """
    STRICT math-only guardrails.

    Returns True ONLY if question strongly looks mathematical.
    Blocks general knowledge / chat / random queries.
    """

    if not question:
        return False

    q = question.lower().strip()

    score = 0

    # --------------------------------------------------
    # 1️⃣ HARD BLOCK (instant reject)
    # --------------------------------------------------
    hard_block = [
        "who", "what is your name", "weather", "news", "movie",
        "actor", "ceo", "president", "capital", "country",
        "history", "sports", "politics", "google", "instagram",
        "chatgpt", "tell me", "explain life", "joke"
    ]

    for word in hard_block:
        if word in q:
            return False


    # --------------------------------------------------
    # 2️⃣ STRONG MATH KEYWORDS (+2)
    # --------------------------------------------------
    strong_keywords = [
        "solve", "equation", "simplify", "factor", "expand",
        "differentiate", "derivative", "integral", "limit",
        "matrix", "determinant", "eigenvalue", "vector",
        "probability", "mean", "median", "variance",
        "theorem", "proof", "function", "graph",
        "series", "sum", "product", "root", "log", "ln"
    ]

    for kw in strong_keywords:
        if re.search(rf"\b{kw}\b", q):
            score += 2


    # --------------------------------------------------
    # 3️⃣ Math symbols (+2)
    # --------------------------------------------------
    if re.search(r"[+\-*/=^<>]", q):
        score += 2


    # --------------------------------------------------
    # 4️⃣ Numbers present (+1)
    # --------------------------------------------------
    if re.search(r"\d+", q):
        score += 1


    # --------------------------------------------------
    # 5️⃣ Algebraic variables (+1)
    # --------------------------------------------------
    if re.search(r"\b[a-z]\b", q):
        score += 1


    # --------------------------------------------------
    # 6️⃣ Trig / calculus patterns (+2)
    # --------------------------------------------------
    if re.search(r"(sin|cos|tan|cot|sec|cosec|ln|log)\s*\(", q):
        score += 2


    # --------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------
    return score >= 2