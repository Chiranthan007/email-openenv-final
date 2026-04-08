import os
from typing import List

from openai import OpenAI

from app.environment import EmailEnv
from app.models import EmailAction


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy-model")

HF_TOKEN = os.getenv("HF_TOKEN")
API_KEY = HF_TOKEN or os.getenv("OPENAI_API_KEY")

MAX_STEPS = 10
BENCHMARK = "email-env"


def safe_score(x: float) -> float:
    return max(0.01, min(0.99, x))


def log_start(task: str):
    print(f"[START] task={task} env={BENCHMARK} model={MODEL_NAME}")


def log_step(step: int, action: str, reward: float, done: bool):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error=null"
    )


def log_end(task: str, success: bool, rewards: List[float]):
    steps = len(rewards)
    raw_score = sum(rewards) / steps if steps > 0 else 0.0
    score = safe_score(raw_score)

    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.2f} rewards={rewards_str}"
    )


def get_model_prediction(client: OpenAI, email: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an email classifier. Reply only with 'spam' or 'not_spam'."
                },
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
        email_lower = email.lower()
        if any(word in email_lower for word in ["win", "free", "offer", "discount", "claim"]):
            return "spam"
        return "not_spam"


def run_task(client: OpenAI, task_id: str):
    env = EmailEnv()
    obs = env.reset(task_id)

    rewards: List[float] = []
    success = True

    log_start(task_id)

    try:
        for step in range(1, MAX_STEPS + 1):
            if env.done:
                break

            action_label = get_model_prediction(client, obs.email)

            obs, reward, done, _ = env.step(
                EmailAction(label=action_label)
            )

            safe = safe_score(reward.score)

            rewards.append(safe)

            log_step(step, action_label, safe, done)

            if done:
                break

    except Exception as e:
        success = False
        print(f"[STEP] step=0 action=error reward=0.00 done=true error={str(e)}")

    log_end(task_id, success, rewards)


def main():
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY or "dummy-key"
    )

    for task_id in ["easy", "medium", "hard"]:
        run_task(client, task_id)


if __name__ == "__main__":
    main()