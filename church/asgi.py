"""
ASGI config for church project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Mount

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church.settings')

# Load Django ASGI
church_app = get_asgi_application()

# Import your FastAPI app
from api.main import app as fastapi_app   # ← adjust path

# Optional: add middleware if you need context / auth between frameworks
class DjangoSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # You can access Django session / user here if needed
        response = await call_next(request)
        return response

fastapi_app.add_middleware(DjangoSessionMiddleware)

# Create combined application
application = Mount(
    path="/",
    routes=[
        Mount("/api", app=fastapi_app),           # ← all /api/* → FastAPI
        Mount("/", app=church_app),                # everything else → Django
    ],
)
