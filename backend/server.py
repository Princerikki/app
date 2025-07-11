from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router

app = FastAPI(
    title="Spark - Dating App API",
    version="1.0.0",
)

# 👉 Root route (your request)
@app.get("/")
async def home():
    return {"message": "Welcome to the Mer API"}

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-frontend-url.com",  # Replace with actual frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your main API router under `/api`
app.include_router(api_router, prefix="/api")
