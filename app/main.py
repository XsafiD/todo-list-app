"""FastAPI application entry point with scheduler integration."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, projects, tasks, reminders, webhooks, stats
from app.config import settings
from app.services.scheduler import scheduler_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown handlers with scheduler lifecycle."""
    # Startup
    print("🚀 Dashboardku starting up...")
    
    # Initialize scheduler service (runs every minute checking deadlines)
    try:
        scheduler_service.init()
    except Exception as e:
        print(f"⚠️ Warning: Failed to initialize scheduler: {e}")
    
    yield
    
    # Shutdown
    print("🔄 Dashboardku shutting down...")
    
    # Gracefully stop scheduler
    try:
        await scheduler_service.shutdown()
    except Exception as e:
        print(f"⚠️ Warning: Error stopping scheduler: {e}")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Dashboardku API",
        description="Personal task management with webhook notifications",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files for frontend
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Include routers (order matters - more specific first)
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(projects.router, prefix="/api", tags=["projects"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(reminders.router, prefix="/api", tags=["reminders"])
    app.include_router(webhooks.router, prefix="/api", tags=["webhooks"])
    app.include_router(stats.router, prefix="/api", tags=["stats"])

    # Serve frontend as default (index.html)
    @app.get("/")
    async def serve_frontend():
        try:
            return FileResponse("app/static/index.html")
        except FileNotFoundError:
            pass

    return app


# Create FastAPI application
app = create_app()


@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "dashboardku"}


@app.get("/scheduler/status", tags=["system"])
async def scheduler_status():
    """Get scheduler status information."""
    from app.services.scheduler import scheduler_service
    
    return {
        "running": scheduler_service._initialized,
        "interval_minutes": 1,
        "last_job_run": None,  # Would track this if needed
    }


# Exception handler
@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    if settings.DEBUG:
        raise
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
