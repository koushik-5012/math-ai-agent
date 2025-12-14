def check_math_guardrails(question: str) -> bool:
    math_keywords = [
        "solve", "equation", "derivative", "integral",
        "matrix", "algebra", "calculus", "geometry",
        "+", "-", "*", "/"
    ]

    q = question.lower()

    for word in math_keywords:
        if word in q:
            return True

    return False
