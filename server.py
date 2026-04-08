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