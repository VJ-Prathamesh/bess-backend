from fastapi import FastAPI
# from app.modules.projects.router import router as projects_router
from app.modules.pv_sizing.router import router as pv_sizing_router
from app.modules.load_profile.router import router
from app.modules.design_assist.router import router as design_router



app = FastAPI()



@app.get("/")
def home():

    return {
        "message":"BESS Backend Running"
    }




app.include_router(pv_sizing_router)

app.include_router(
    router,
    prefix="/load-profile",
    tags=["Load Profile"]
)



app.include_router(
    design_router,
    prefix="/design-assist",
    tags=["Design Assist"]
)

