from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    metrics = relationship("HealthMetric", back_populates="user")

class HealthMetric(Base):
    __tablename__ = "health_metrics"

    metric_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, index=True)
    steps = Column(Integer)
    calories = Column(Float)
    heart_rate = Column(Integer)

    user = relationship("User", back_populates="metrics")

class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    metric_type = Column(String) # e.g., 'steps', 'calories'
    target_value = Column(Integer)
    
    user = relationship("User", back_populates="goals")

# Update User relationship to include goals
User.goals = relationship("Goal", back_populates="user")

