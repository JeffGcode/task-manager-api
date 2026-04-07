import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import users, tasks, categories

app = FastAPI(title="Task Manager API", version="1.0.0")

# Custom OpenAPI schema to replace OAuth2PasswordBearer with simple HTTPBearer
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Task Manager API",
        version="1.0.0",
        routes=app.routes,
    )
    # Replace the security scheme with HTTP Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply the new security scheme to all endpoints that originally had security
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" in method:
                method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)

@app.get("/")
def root():
    return {"message": "Task Manager API"}

# This block is used when running the script directly (e.g., with `python main.py`).
# On Railway, the `uvicorn` command will be used instead, but this ensures the app
# can also be started with a simple `python app/main.py` and will respect the PORT env var.
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)