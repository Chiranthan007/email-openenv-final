from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.environment import EmailEnv
from app.models import EmailAction


app = FastAPI()  # MUST be defined before any decorators

env = None


class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"


class StepRequest(BaseModel):
    action: str


@app.get("/")
def home():
    return {"message": "Email Env API is running"}


@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    global env
    try:
        env = EmailEnv()

        task_id = req.task_id or "easy"
        obs = env.reset(task_id)

        return {
            "email": obs.email
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/step")
def step(req: StepRequest):
    global env
    try:
        if env is None or env.task is None:
            return {"error": "Call /reset first"}

        obs, reward, done, _ = env.step(
            EmailAction(label=req.action)
        )

        return {
            "email": obs.email,
            "reward": reward.score,
            "done": done
        }

    except Exception as e:
        return {"error": str(e)}