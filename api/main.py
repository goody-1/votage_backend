# yourproject/api/main.py
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Optional: reuse Django settings / models
from django.conf import settings

from fastapi.middleware.cors import CORSMiddleware
from .routers import home, auth, members, pastors, services, attendance, events, connect_groups, growth_track, departments, dashboard

app = FastAPI(
    title="Votage Church API",
    description="Manage church data like members, attendance, growth tracks, and more.",
    version="0.1.0",
    docs_url="/docs",           # http://127.0.0.1:8000/api/docs
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include each router – they will be mounted under their own prefix
app.include_router(auth.router)
app.include_router(home.router)
app.include_router(members.router)
app.include_router(pastors.router)
app.include_router(services.router)
app.include_router(attendance.router)
app.include_router(events.router)
app.include_router(connect_groups.router)
app.include_router(growth_track.router)
app.include_router(departments.router)
app.include_router(dashboard.router)



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
