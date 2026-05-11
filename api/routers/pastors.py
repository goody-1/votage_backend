from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from apps.pastors.models import Pastor
from ..schemas.pastors import PastorCreate, PastorUpdate, PastorOut
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/pastors",
    tags=["Pastors"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=List[PastorOut])
def list_pastors():
    return [PastorOut.from_orm(p) for p in Pastor.objects.all()]

@router.post("/", response_model=PastorOut, status_code=status.HTTP_201_CREATED)
def create_pastor(pastor_in: PastorCreate):
    pastor = Pastor.objects.create(**pastor_in.dict())
    return PastorOut.from_orm(pastor)

@router.get("/{pastor_id}", response_model=PastorOut)
def get_pastor(pastor_id: int):
    try:
        return PastorOut.from_orm(Pastor.objects.get(pk=pastor_id))
    except Pastor.DoesNotExist:
        raise HTTPException(status_code=404, detail="Pastor not found")

@router.patch("/{pastor_id}", response_model=PastorOut)
def update_pastor(pastor_id: int, pastor_in: PastorUpdate):
    try:
        pastor = Pastor.objects.get(pk=pastor_id)
        update_data = pastor_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pastor, field, value)
        pastor.save()
        return PastorOut.from_orm(pastor)
    except Pastor.DoesNotExist:
        raise HTTPException(status_code=404, detail="Pastor not found")

@router.delete("/{pastor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pastor(pastor_id: int):
    try:
        Pastor.objects.get(pk=pastor_id).delete()
        return None
    except Pastor.DoesNotExist:
        raise HTTPException(status_code=404, detail="Pastor not found")
