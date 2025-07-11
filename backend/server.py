from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mer - Dating App API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Mer API"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
