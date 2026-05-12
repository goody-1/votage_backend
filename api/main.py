# yourproject/api/main.py
import os
import django

# Initialize Django before any other imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "church.settings")
django.setup()

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Optional: reuse Django settings / models
from django.conf import settings

from fastapi.middleware.cors import CORSMiddleware
from .routers import home, auth, members, pastors, services, attendance, events, connect_groups, growth_track, departments, dashboard

app = FastAPI(
    title="Votage Church API",
    description="Manage church data like members, attendance, growth tracks, and more.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

from starlette.middleware.sessions import SessionMiddleware

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Set to False to allow "*" origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include each router – they will be mounted under /api
app.include_router(auth.router, prefix="/api")
app.include_router(home.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(pastors.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(connect_groups.router, prefix="/api")
app.include_router(growth_track.router, prefix="/api")
app.include_router(departments.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Mount Django Admin
from django.core.wsgi import get_wsgi_application
from fastapi.middleware.wsgi import WSGIMiddleware
app.mount("/admin", WSGIMiddleware(get_wsgi_application()))

# Serve static files (ensure 'staticfiles' directory exists after running collectstatic)
from django.conf import settings
if settings.STATIC_ROOT.exists():
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_ROOT)), name="static")



class PingResponse(BaseModel):
    status: str = "ok"
    environment: str

@app.get("/ping", response_model=PingResponse)
async def ping():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT if hasattr(settings, "ENVIRONMENT") else "unknown"
    }

# Example with Django ORM (optional)
# @app.get("/members/count")
# async def members_count():
#     from members.models import Member
#     return {"total_members": Member.objects.count()}
