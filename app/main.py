from fastapi import FastAPI

from modules.projects.router import router as project_router
from modules.location_weather.router import router as location_router

app = FastAPI(title="BESS Backend")

app.include_router(project_router)
app.include_router(location_router)


# from fastapi import FastAPI

# from modules.projects.router import router as project_router
# from modules.location_weather.router import router as location_router

# app = FastAPI(
#     title="BESS Backend",
#     version="1.0.0"
# )

# Register Routers
# app.include_router(project_router)
# app.include_router(location_router)


# ── Root ──────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Welcome to BESS Backend API",
        "status": "Running"
    }
