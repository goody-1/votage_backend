from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from apps.connect_groups.models import ConnectGroup, ConnectGroupMember, ConnectGroupPastor
from ..schemas.connect_groups import (
    ConnectGroupCreate, ConnectGroupUpdate, ConnectGroupOut,
    ConnectGroupMemberCreate, ConnectGroupMemberOut,
    ConnectGroupPastorCreate, ConnectGroupPastorOut
)
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/connect-groups",
    tags=["Connect Groups"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=List[ConnectGroupOut])
def list_connect_groups():
    return [ConnectGroupOut.from_orm(cg) for cg in ConnectGroup.objects.all()]

@router.post("/", response_model=ConnectGroupOut, status_code=status.HTTP_201_CREATED)
def create_connect_group(cg_in: ConnectGroupCreate):
    cg = ConnectGroup.objects.create(**cg_in.dict())
    return ConnectGroupOut.from_orm(cg)

# Members
@router.get("/{cg_id}/members/", response_model=List[ConnectGroupMemberOut])
def list_cg_members(cg_id: int):
    return [ConnectGroupMemberOut.from_orm(m) for m in ConnectGroupMember.objects.filter(connect_group_id=cg_id).select_related("member")]

@router.post("/members/", response_model=ConnectGroupMemberOut)
def add_cg_member(m_in: ConnectGroupMemberCreate):
    m = ConnectGroupMember.objects.create(**m_in.dict())
    return ConnectGroupMemberOut.from_orm(m)

# Pastors
@router.get("/{cg_id}/pastors/", response_model=List[ConnectGroupPastorOut])
def list_cg_pastors(cg_id: int):
    return [ConnectGroupPastorOut.from_orm(p) for p in ConnectGroupPastor.objects.filter(connect_group_id=cg_id).select_related("pastor")]

@router.post("/pastors/", response_model=ConnectGroupPastorOut)
def add_cg_pastor(p_in: ConnectGroupPastorCreate):
    p = ConnectGroupPastor.objects.create(**p_in.dict())
    return ConnectGroupPastorOut.from_orm(p)
