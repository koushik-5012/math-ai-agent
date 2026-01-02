import re

TOPIC_RULES = {
    "algebra": [
        r"\bsolve\b", r"\bequation\b", r"[a-zA-Z]\s*=", r"\bx\b"
    ],
    "calculus": [
        r"\bderivative\b", r"\bdifferentiate\b", r"\bintegral\b", r"\blimit\b",
        r"\bdx\b", r"\bdy\b", r"∫"
    ],
    "trigonometry": [
        r"\bsin\b", r"\bcos\b", r"\btan\b", r"\bcot\b", r"\bsec\b", r"\bcosec\b"
    ],
    "linear_algebra": [
        r"\bmatrix\b", r"\bvector\b", r"\beigen\b", r"\bdeterminant\b"
    ],
    "number_theory": [
        r"\blcm\b", r"\bhcf\b", r"\bgcd\b", r"\bremainder\b", r"\bdivisible\b"
    ],
    "probability": [
        r"\bprobability\b", r"\bmean\b", r"\bvariance\b", r"\bmedian\b"
    ],
    "geometry": [
        r"\btriangle\b", r"\bcircle\b", r"\barea\b", r"\bperimeter\b"
    ]
}

def detect_topic(text: str) -> str:
    text = text.lower()

    for topic, patterns in TOPIC_RULES.items():
        for pat in patterns:
            if re.search(pat, text):
                return topic

    return "unknown"


def parse_problem(raw_text: str):
    topic = detect_topic(raw_text)

    needs_clarification = topic == "unknown"

    return {
        "problem_text": raw_text.strip(),
        "topic": topic,
        "needs_clarification": needs_clarification
    }
