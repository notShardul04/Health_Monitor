from pydantic import BaseModel
from typing import Optional
from datetime import date

# User Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# HealthMetric Schemas
class HealthMetricBase(BaseModel):
    date: date
    steps: int
    calories: float
    heart_rate: int

class HealthMetricCreate(HealthMetricBase):
    pass

class HealthMetric(HealthMetricBase):
    metric_id: int
    user_id: int

    model_config = {"from_attributes": True}

# Goal Schemas
class GoalBase(BaseModel):
    metric_type: str
    target_value: int

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    goal_id: int
    user_id: int

    model_config = {"from_attributes": True}

class GoalProgress(BaseModel):
    metric_type: str
    target_value: int
    current_value: float
    percentage: float
