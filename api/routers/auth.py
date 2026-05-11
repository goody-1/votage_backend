from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from django.contrib.auth import authenticate
from ..deps import create_access_token
from ..schemas.auth import Token, UserOut

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

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate):
    if User.objects.filter(username=user_in.username).exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    if User.objects.filter(email=user_in.email).exists():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User.objects.create_user(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password
    )
    return user

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user
