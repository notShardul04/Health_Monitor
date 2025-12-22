from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Annotated

import os
from jose import JWTError, jwt
from passlib.context import CryptContext

import models
import schemas
import database

# Database Initialization
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Health & Fitness Monitor")

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeyShouldBeChangeInProduction")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Helper Functions ---

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# --- Auth Endpoints ---

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.refresh(new_user)
    return new_user

@app.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user

# --- Health Metrics CRUD ---

@app.post("/metrics", response_model=schemas.HealthMetric)
def create_metric(
    metric: schemas.HealthMetricCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(database.get_db)
):
    # Verify date uniqueness for user if desired, strictly prompt only asked for CRUD.
    # We'll allow multiple entries per day or just insert.
    db_metric = models.HealthMetric(**metric.dict(), user_id=current_user.id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@app.get("/metrics", response_model=List[schemas.HealthMetric])
def read_metrics(
    current_user: Annotated[models.User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    metrics = db.query(models.HealthMetric).filter(models.HealthMetric.user_id == current_user.id).offset(skip).limit(limit).all()
    return metrics

@app.delete("/metrics/{metric_id}")
def delete_metric(
    metric_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(database.get_db)
):
    metric = db.query(models.HealthMetric).filter(models.HealthMetric.metric_id == metric_id, models.HealthMetric.user_id == current_user.id).first()
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()
    db.delete(metric)
    db.commit()
    return {"ok": True}

# --- Goals Endpoints ---

@app.post("/goals", response_model=schemas.Goal)
def create_or_update_goal(
    goal: schemas.GoalCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(database.get_db)
):
    # Check if goal exists for this metric type
    db_goal = db.query(models.Goal).filter(models.Goal.user_id == current_user.id, models.Goal.metric_type == goal.metric_type).first()
    if db_goal:
        db_goal.target_value = goal.target_value
        db.commit()
        db.refresh(db_goal)
        return db_goal
    
    new_goal = models.Goal(**goal.dict(), user_id=current_user.id)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@app.get("/goals/progress", response_model=List[schemas.GoalProgress])
def get_goals_progress(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(database.get_db)
):
    goals = db.query(models.Goal).filter(models.Goal.user_id == current_user.id).all()
    results = []
    
    # Get today's metrics
    today = datetime.now().date()
    # Assuming one entry per day, or sum of entries
    # Simple approach: sum all entries for today
    today_metrics = db.query(models.HealthMetric).filter(models.HealthMetric.user_id == current_user.id, models.HealthMetric.date == today).all()
    
    total_steps = sum([m.steps for m in today_metrics])
    total_calories = sum([m.calories for m in today_metrics])
    
    for goal in goals:
        current_val = 0
        if goal.metric_type == "steps":
            current_val = total_steps
        elif goal.metric_type == "calories":
            current_val = total_calories
            
        percentage = 0
        if goal.target_value > 0:
            percentage = min(current_val / goal.target_value * 100, 100) # Cap at 100 or allow overflow? Gauge usually likes 0-1 or 0-100. Let's keep raw % but maybe cap for UI or let UI handle. 
            # Actually, let's allow > 100 for "overachiever" status, but limit check logic.
            percentage = (current_val / goal.target_value) * 100

        results.append(schemas.GoalProgress(
            metric_type=goal.metric_type,
            target_value=goal.target_value,
            current_value=current_val,
            percentage=percentage
        ))
        
    return results


