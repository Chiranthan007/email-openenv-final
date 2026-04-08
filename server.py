from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.environment import EmailEnv
from app.models import EmailAction

app = FastAPI()

# Keep env global but initialize later
env = None


# Request models
class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"


class StepRequest(BaseModel):
    action: str


# Root route (prevents 404 at "/")
@app.get("/")
def home():
    return {"message": "Email Env API is running"}


# Reset endpoint
@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    global env
    try:
        env = EmailEnv()  # initialize here safely

        task_id = req.task_id or "easy"
        obs = env.reset(task_id)

        return {
            "email": obs.email,
            "step_count": obs.step_count
        }

    except Exception as e:
        return {"error": str(e)}


# Step endpoint
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
            "done": done,
            "step_count": obs.step_count
        }

    except Exception as e:
        return {"error": str(e)}