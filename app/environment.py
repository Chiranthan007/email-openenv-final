from app.tasks import TASKS
from app.graders import grade_email
from app.models import EmailObservation, EmailAction, EmailReward


class EmailEnv:
    def __init__(self):
        self.task = None
        self.current_index = 0
        self.done = False

    def reset(self, task_id: str = "easy"):
        self.task = None

        for t in TASKS:
            if t["id"] == task_id:
                self.task = t
                break

        if self.task is None:
            raise ValueError(f"Invalid task_id: {task_id}")

        self.current_index = 0
        self.done = False

        first_email = self.task["emails"][self.current_index]["text"]

        return EmailObservation(
            email=first_email,
            step_count=0
        )

    def step(self, action: EmailAction):
        if self.done:
            raise Exception("Episode already finished")

        current_email_data = self.task["emails"][self.current_index]
        true_label = current_email_data["label"]

        # Calculate reward
        score = grade_email(action.label, true_label)
        reward = EmailReward(score=score)

        # Move to next email
        self.current_index += 1

        # Check if done
        if self.current_index >= len(self.task["emails"]):
            self.done = True
            next_email = ""
        else:
            next_email = self.task["emails"][self.current_index]["text"]

        observation = EmailObservation(
            email=next_email,
            step_count=self.current_index
        )

        return observation, reward, self.done, {}

    def state(self):
        return {
            "task_id": self.task["id"] if self.task else None,
            "current_index": self.current_index,
            "done": self.done
        }