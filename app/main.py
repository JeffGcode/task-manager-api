from fastapi import FastAPI
from app.routers import users, tasks, categories

app = FastAPI(title="Task Manager API", version="1.0.0")

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)

@app.get("/")
def root():
    return {"message": "Task Manager API"}