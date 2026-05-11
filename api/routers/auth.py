from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from django.contrib.auth import authenticate
from ..deps import create_access_token
from ..schemas.auth import Token, UserOut, RegistrationResponse
from authlib.integrations.starlette_client import OAuth
import os
from django.conf import settings
from fastapi import Request
from starlette.responses import RedirectResponse

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(subject=user.pk)
    return {"access_token": access_token, "token_type": "bearer"}

from ..deps import get_current_user, get_password_hash
from ..schemas.auth import Token, UserOut, UserCreate
from django.contrib.auth.models import User

@router.post("/register", response_model=RegistrationResponse)
def register(user_in: UserCreate):
    if User.objects.filter(username=user_in.username).exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    if User.objects.filter(email=user_in.email).exists():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user with is_active=False for admin approval
    user = User.objects.create_user(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        is_active=False
    )
    return {
        "user": user,
        "message": "Account created successfully. Please wait for an administrator to approve your access."
    }

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/google/login")
async def google_login(request: Request):
    # Determine callback URL (handle Render HTTPS forwarding if necessary)
    redirect_uri = request.url_for('auth:google_callback')
    if 'onrender.com' in str(request.base_url) and redirect_uri.startswith('http://'):
        redirect_uri = redirect_uri.replace('http://', 'https://')
    
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")
        
    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info from Google")
    
    email = user_info.get('email')
    username = user_info.get('name', email.split('@')[0])
    
    # Get or create user
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            'is_active': False  # Still requires admin approval!
        }
    )
    
    if not user.is_active:
        return {
            "message": "Login successful, but your account is pending administrator approval.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }
        }

    # Generate JWT for active users
    access_token = create_access_token(subject=user.pk)
    return {"access_token": access_token, "token_type": "bearer"}
