from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

# User
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    from app.auth import get_password_hash
    hashed = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Category
def get_categories(db: Session, skip: int = 0, limit: int = 100, owner_id: int = None):
    query = db.query(models.Category)
    if owner_id:
        query = query.filter(models.Category.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate, owner_id: int):
    db_category = models.Category(**category.model_dump(), owner_id=owner_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, owner_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id, models.Category.owner_id == owner_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

# Task
def get_tasks(db: Session, skip: int = 0, limit: int = 100, owner_id: int = None, category_id: int = None):
    query = db.query(models.Task)
    if owner_id:
        query = query.filter(models.Task.owner_id == owner_id)
    if category_id:
        query = query.filter(models.Task.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, owner_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, owner_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == owner_id).first()
    if not db_task:
        return None
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, owner_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == owner_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False