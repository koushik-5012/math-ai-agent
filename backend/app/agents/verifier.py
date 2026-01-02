import re

def verify_answer(answer: str) -> dict:
    """
    Lightweight verification heuristics.
    """

    if not answer or len(answer.strip()) < 5:
        return {
            "is_correct": False,
            "confidence": 0.1
        }

    # If it contains numeric result or algebraic form
    math_signal = re.search(r"\b\d+\b|x\s*=", answer.lower())

    if math_signal:
        return {
            "is_correct": True,
            "confidence": 0.85
        }

    # If it is too vague
    return {
        "is_correct": False,
        "confidence": 0.3
    }
