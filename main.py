from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router

app = FastAPI(
    title="Startapusai API",
    description="AI-акселератор концепцій",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшені замінимо на домени нашого WordPress сайту
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Startapusai API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
