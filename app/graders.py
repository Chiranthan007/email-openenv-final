def grade_email(predicted_label: str, true_label: str) -> float:
    predicted_label = predicted_label.lower().strip()
    true_label = true_label.lower().strip()

    if predicted_label == true_label:
        return 0.95

    if predicted_label in ["spam", "not_spam"]:
        return 0.4

    return 0.05