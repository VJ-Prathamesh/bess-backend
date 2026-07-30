from fastapi import FastAPI
# from app.modules.projects.router import router as projects_router
from app.modules.pv_sizing.router import router as pv_sizing_router

app = FastAPI()
# app.include_router(projects_router)
app.include_router(pv_sizing_router)
