from pydantic import BaseModel


class EmailObservation(BaseModel):
    email: str


class EmailAction(BaseModel):
    label: str


class EmailReward(BaseModel):
    score: float