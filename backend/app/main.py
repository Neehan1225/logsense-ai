from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models.log_entry import Base
from app.api import logs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,       
    version=settings.APP_VERSION,
    description="AI-powered log analysis platform using Gemini AI",
    
    docs_url="/docs",     
    redoc_url="/redoc"     
)

app.add_middleware(
    CORSMiddleware,
    
    allow_origins=["*"],
    
    allow_credentials=True,
    
    allow_methods=["*"],
    
    
    allow_headers=["*"],
)

app.include_router(logs.router, prefix="/api/v1")

@app.get("/")
def root():
    """Health check endpoint — confirms the API is running."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
def health_check():
    """
    Used by Docker, AWS load balancers, and monitoring tools
    to check if the service is alive and responding.
    """
    return {"status": "healthy", "app": settings.APP_NAME}