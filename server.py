from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.environment import EmailEnv
from app.models import EmailAction

app = FastAPI()

env = EmailEnv()


# ✅ Make task_id OPTIONAL
class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"


class StepRequest(BaseModel):
    action: str


@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    try:
        # fallback if empty request
        task_id = req.task_id or "easy"

        obs = env.reset(task_id)

        return {
            "email": obs.email,
            "step_count": obs.step_count
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/step")
def step(req: StepRequest):
    try:
        # prevent step before reset
        if env.task is None:
            return {"error": "Call /reset first"}

        obs, reward, done, _ = env.step(
            EmailAction(label=req.action)
        )

        return {
            "email": obs.email,
            "reward": reward.score,
            "done": done,
            "step_count": obs.step_count
        }

    except Exception as e:
        return {
            "error": str(e)
        }