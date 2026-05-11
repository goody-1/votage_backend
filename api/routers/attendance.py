from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.attendance.models import Attendance
from ..schemas.attendance import AttendanceCreate, AttendanceOut
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=List[AttendanceOut])
def list_attendance(service_id: Optional[int] = None):
    queryset = Attendance.objects.all().select_related("member", "service")
    if service_id:
        queryset = queryset.filter(service_id=service_id)
    return [AttendanceOut.from_orm(a) for a in queryset.order_by("-created_at")]

@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def record_attendance(attendance_in: AttendanceCreate):
    try:
        attendance = Attendance.objects.create(**attendance_in.dict())
        return AttendanceOut.from_orm(attendance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: int):
    try:
        Attendance.objects.get(pk=attendance_id).delete()
        return None
    except Attendance.DoesNotExist:
        raise HTTPException(status_code=404, detail="Attendance record not found")
