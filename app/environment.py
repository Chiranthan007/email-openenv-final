from app.tasks import TASKS
from app.models import EmailObservation, EmailAction, EmailReward


class EmailEnv:
    def __init__(self):
        self.task = None
        self.current_index = 0
        self.done = False

        # NEW internal state
        self.correct = 0
        self.total = 0
        self.mistakes = 0
        self.max_mistakes = 3

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

        # reset stats
        self.correct = 0
        self.total = 0
        self.mistakes = 0

        first_email = self.task["emails"][self.current_index]["text"]

        return EmailObservation(email=first_email)

    def step(self, action: EmailAction):
        if self.done:
            raise Exception("Episode already finished")

        current_email_data = self.task["emails"][self.current_index]
        true_label = current_email_data["label"]

        predicted = action.label.lower().strip()
        true_label = true_label.lower().strip()

        # ---- BASE REWARD ----
        if predicted == true_label:
            base = 0.95
            self.correct += 1
        elif predicted in ["spam", "not_spam"]:
            base = 0.4
            self.mistakes += 1
        else:
            base = 0.05
            self.mistakes += 1

        self.total += 1

        # ---- SHAPING ----
        accuracy = self.correct / self.total if self.total > 0 else 0
        bonus = 0.04 * accuracy
        penalty = 0.02 * self.mistakes

        score = base + bonus - penalty

        # clamp strictly (0,1)
        score = min(0.99, max(0.01, score))

        reward = EmailReward(score=score)

        # ---- NEXT STEP ----
        self.current_index += 1

        # early stop if too many mistakes
        if self.mistakes >= self.max_mistakes:
            self.done = True

        if self.current_index >= len(self.task["emails"]):
            self.done = True
            next_email = ""
        else:
            next_email = self.task["emails"][self.current_index]["text"]

        observation = EmailObservation(email=next_email)

        return observation, reward, self.done, {}