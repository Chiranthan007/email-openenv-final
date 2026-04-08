def grade_email(predicted_label: str, true_label: str) -> float:
    """
    Returns a score between 0.0 and 1.0
    """

    predicted_label = predicted_label.lower().strip()
    true_label = true_label.lower().strip()

    # Exact match
    if predicted_label == true_label:
        return 1.0

    # Partial logic: if agent at least outputs valid label
    if predicted_label in ["spam", "not_spam"]:
        return 0.3

    # Completely wrong / invalid output
    return 0.0