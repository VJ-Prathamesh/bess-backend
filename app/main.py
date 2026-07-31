from fastapi import FastAPI

# Upstream module routers
# from app.modules.projects.router import router as projects_router
from app.modules.pv_sizing.router import router as pv_sizing_router
from app.modules.load_profile.router import router as load_profile_router
from app.modules.design_assist.router import router as design_router

# Simulation & BOQ model registration (ensures tables are created)
import app.modules.boq.models
import app.modules.projects.models
import app.modules.simulation.models

# Core DB setup
from app.core.database import Base, engine

# Simulation & BOQ routers
from app.modules.boq.router import router as boq_router
from app.modules.simulation.router import router as simulation_router

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BESS Backend",
    version="1.0.0"
)

# ── Root ──────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "BESS Backend Running"}

# ── Upstream module routers ───────────────────────────────────────
app.include_router(pv_sizing_router)

app.include_router(
    load_profile_router,
    prefix="/load-profile",
    tags=["Load Profile"]
)

app.include_router(
    design_router,
    prefix="/design-assist",
    tags=["Design Assist"]
)

# ── Simulation & BOQ routers ──────────────────────────────────────
app.include_router(simulation_router)
app.include_router(boq_router)
