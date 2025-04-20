from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.api import chat

app = FastAPI(
    title="E-commerce Customer Service Agent",
    description="AI-powered customer service agent for e-commerce platforms",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Include chat router
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html") 