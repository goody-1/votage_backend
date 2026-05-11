from fastapi import APIRouter

router = APIRouter(
    prefix="/home",          # all endpoints in this router start with /home
    tags=["Home"],           # groups them nicely in /docs
)

@router.get("/", summary="Home / Dashboard overview")
async def home_overview():
    return {"message": "Welcome to the Church Dashboard", "version": "0.1"}

@router.get("/stats")
async def home_stats():
    return {"active_members": 150, "today_attendance": 87}
