TASKS = [
    {
        "id": "easy",
        "description": "Classify obvious spam vs normal email",
        "emails": [
            {"text": "Win a free iPhone now!", "label": "spam"},
            {"text": "Meeting at 3pm tomorrow", "label": "not_spam"},
        ],
    },
    {
        "id": "medium",
        "description": "Classify promotional vs legitimate service emails",
        "emails": [
            {"text": "Limited time discount just for you", "label": "spam"},
            {"text": "Your order has been shipped", "label": "not_spam"},
        ],
    },
    {
        "id": "hard",
        "description": "Detect subtle phishing attempts",
        "emails": [
            {"text": "Update your account to avoid suspension", "label": "spam"},
            {"text": "Quarterly performance report attached", "label": "not_spam"},
        ],
    },
]