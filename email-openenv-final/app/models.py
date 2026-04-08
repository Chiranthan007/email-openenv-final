from pydantic import BaseModel


class EmailObservation(BaseModel):
    email: str
    step_count: int


class EmailAction(BaseModel):
    label: str  # "spam" or "not_spam"


class EmailReward(BaseModel):
    score: float  # 0.0 to 1.0