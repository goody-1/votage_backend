from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from apps.growth_track.models import GrowthTrack, GrowthTrackEnrollment
from ..schemas.growth_track import (
    GrowthTrackCreate, GrowthTrackUpdate, GrowthTrackOut,
    GrowthTrackEnrollmentCreate, GrowthTrackEnrollmentOut
)
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/growth-tracks",
    tags=["Growth Track"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=List[GrowthTrackOut])
def list_growth_tracks():
    return [GrowthTrackOut.from_orm(gt) for gt in GrowthTrack.objects.all()]

@router.post("/", response_model=GrowthTrackOut, status_code=status.HTTP_201_CREATED)
def create_growth_track(gt_in: GrowthTrackCreate):
    gt = GrowthTrack.objects.create(**gt_in.dict())
    return GrowthTrackOut.from_orm(gt)

# Enrollments
@router.get("/{gt_id}/enrollments/", response_model=List[GrowthTrackEnrollmentOut])
def list_enrollments(gt_id: int):
    return [GrowthTrackEnrollmentOut.from_orm(e) for e in GrowthTrackEnrollment.objects.filter(growth_track_id=gt_id).select_related("member")]

@router.post("/enrollments/", response_model=GrowthTrackEnrollmentOut)
def enroll_member(e_in: GrowthTrackEnrollmentCreate):
    e = GrowthTrackEnrollment.objects.create(**e_in.dict())
    return GrowthTrackEnrollmentOut.from_orm(e)
