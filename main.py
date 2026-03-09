from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai

app = FastAPI(title="JobTrackr API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/ai", tags=["AI"])

@app.get("/health")
def health():
    return {"status": "ok"}
