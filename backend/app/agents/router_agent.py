def route_intent(parsed: dict) -> str:
    """
    Decide which agent should handle the problem.
    """

    topic = parsed.get("topic", "unknown")
    needs_clarification = parsed.get("needs_clarification", False)

    if needs_clarification:
        return "clarification_agent"

    if topic in ["algebra", "calculus", "trigonometry", "linear_algebra", "number_theory", "probability", "geometry"]:
        return "math_solver"

    return "fallback_agent"
