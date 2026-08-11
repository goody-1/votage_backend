from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from django.db.models import Q
from apps.members.models import Member, FirstTimers
from ..schemas.members import MemberCreate, MemberUpdate, MemberOut, FirstTimerCreate, FirstTimerOut
from ..pagination import PaginatedResponse, paginate
from ..deps import get_current_admin_user

from uuid import UUID

router = APIRouter(
    prefix="/members",
    tags=["Members"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=PaginatedResponse[MemberOut])
def list_members(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    gender: Optional[str] = None,
    is_worker: Optional[bool] = None,
):
    queryset = Member.objects.all().order_by("-id")
    
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(phone_number__icontains=search)
        )
    
    if gender:
        queryset = queryset.filter(gender=gender)

    if is_worker is True:
        queryset = queryset.filter(departmentmembership__is_active=True).distinct()
    elif is_worker is False:
        queryset = queryset.exclude(departmentmembership__is_active=True)
    
    paginated_data = paginate(queryset, page, page_size)
    paginated_data["results"] = [MemberOut.from_orm(m) for m in paginated_data["results"]]
    return paginated_data

@router.post("/", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(member_in: MemberCreate):
    member = Member.objects.create(**member_in.dict())
    return MemberOut.from_orm(member)

@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: UUID):
    try:
        member = Member.objects.get(pk=member_id)
        return MemberOut.from_orm(member)
    except Member.DoesNotExist:
        raise HTTPException(status_code=404, detail="Member not found")

@router.patch("/{member_id}", response_model=MemberOut)
def update_member(member_id: UUID, member_in: MemberUpdate):
    try:
        member = Member.objects.get(pk=member_id)
        update_data = member_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(member, field, value)
        member.save()
        return MemberOut.from_orm(member)
    except Member.DoesNotExist:
        raise HTTPException(status_code=404, detail="Member not found")

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: UUID):
    try:
        member = Member.objects.get(pk=member_id)
        member.delete()
        return None
    except Member.DoesNotExist:
        raise HTTPException(status_code=404, detail="Member not found")

# First Timers
@router.get("/first-timers/", response_model=List[FirstTimerOut])
def list_first_timers():
    ft = FirstTimers.objects.all().order_by("-created_at")[:100]
    return [FirstTimerOut.from_orm(f) for f in ft]

@router.post("/first-timers/", response_model=FirstTimerOut, status_code=status.HTTP_201_CREATED)
def create_first_timer(ft_in: FirstTimerCreate):
    ft = FirstTimers.objects.create(**ft_in.dict())
    return FirstTimerOut.from_orm(ft)
