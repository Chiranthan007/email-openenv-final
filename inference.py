import os
from typing import List
from openai import OpenAI

from app.environment import EmailEnv
from app.models import EmailAction


# Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy-model")
API_KEY = os.getenv("OPENAI_API_KEY", "dummy-key")

MAX_STEPS = 10


def log_start(task: str):
    print(f"[START] task={task}")


def log_step(step: int, action: str, reward: float, done: bool):
    print(f"[STEP] step={step} action={action} reward={reward} done={done}")


def log_end(task: str, score: float):
    print(f"[END] task={task} score={score}")


def get_model_prediction(client: OpenAI, email: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an email classifier. Reply only with 'spam' or 'not_spam'."},
                {"role": "user", "content": email},
            ],
            max_tokens=5,
            temperature=0,
        )

        text = (response.choices[0].message.content or "").strip().lower()

        if "spam" in text:
            return "spam"
        return "not_spam"

    except Exception:
        # Fallback (important for offline / no API)
        email_lower = email.lower()
        if any(word in email_lower for word in ["win", "free", "offer", "discount", "claim"]):
            return "spam"
        return "not_spam"


def run_task(client: OpenAI, task_id: str):
    env = EmailEnv()
    obs = env.reset(task_id)

    rewards: List[float] = []

    log_start(task_id)

    for step in range(1, MAX_STEPS + 1):
        if env.done:
            break

        action_label = get_model_prediction(client, obs.email)

        obs, reward, done, _ = env.step(EmailAction(label=action_label))

        rewards.append(reward.score)

        log_step(step, action_label, reward.score, done)

        if done:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.0
    log_end(task_id, score)


def main():
    # OpenAI client (required by spec)
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task_id in ["easy", "medium", "hard"]:
        run_task(client, task_id)


if __name__ == "__main__":
    main()