from fastapi import FastAPI

app = FastAPI(
    title="BESS Backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to BESS Backend"
    }