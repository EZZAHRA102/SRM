"""FastAPI application entry point."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api.routes import health, chat, ocr
from backend.api.deps import get_agent
from backend.logging_config import setup_logging

# Create FastAPI app
app = FastAPI(
    title="SRM API",
    description="SRM Water & Electricity Utility Customer Service API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(ocr.router, prefix="/api", tags=["ocr"])


@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup."""
    try:
        agent = get_agent()
        if not agent:
            raise RuntimeError("Failed to initialize agent")
    except Exception as e:
        print(f"Warning: Agent initialization failed: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SRM API",
        "version": "1.0.0",
        "docs": "/docs"
    }


