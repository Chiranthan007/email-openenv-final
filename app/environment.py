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

        return EmailObservation(email=first_email)

    def step(self, action: EmailAction):
        if self.done:
            raise Exception("Episode already finished")

        current_email_data = self.task["emails"][self.current_index]
        true_label = current_email_data["label"]

        score = grade_email(action.label, true_label)
        reward = EmailReward(score=score)

        self.current_index += 1

        if self.current_index >= len(self.task["emails"]):
            self.done = True
            next_email = ""
        else:
            next_email = self.task["emails"][self.current_index]["text"]

        observation = EmailObservation(email=next_email)

        return observation, reward, self.done, {}