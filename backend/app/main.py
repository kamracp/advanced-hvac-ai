from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import calculators, extras

app = FastAPI(
    title="Advanced HVAC AI API",
    description="Indian SI HVAC Engineering Platform - Kamra Engineering Solutions",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your actual frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculators.router)
app.include_router(extras.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Advanced HVAC AI API is running. See /docs for API documentation."}
