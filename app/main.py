from fastapi import FastAPI
from app.modules.projects.router import router as projects_router

app = FastAPI()
app.include_router(projects_router)