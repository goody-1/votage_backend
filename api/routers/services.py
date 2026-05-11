from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from apps.services.models import Service, ServiceType
from ..schemas.services import ServiceCreate, ServiceUpdate, ServiceOut, ServiceTypeCreate, ServiceTypeOut
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/services",
    tags=["Services"],
    dependencies=[Depends(get_current_admin_user)]
)

# Service Types
@router.get("/types/", response_model=List[ServiceTypeOut])
def list_service_types():
    return [ServiceTypeOut.from_orm(st) for st in ServiceType.objects.all()]

@router.post("/types/", response_model=ServiceTypeOut, status_code=status.HTTP_201_CREATED)
def create_service_type(st_in: ServiceTypeCreate):
    st = ServiceType.objects.create(**st_in.dict())
    return ServiceTypeOut.from_orm(st)

# Services
@router.get("/", response_model=List[ServiceOut])
def list_services():
    return [ServiceOut.from_orm(s) for s in Service.objects.all().select_related("service_type")]

@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(service_in: ServiceCreate):
    service = Service.objects.create(**service_in.dict())
    return ServiceOut.from_orm(service)

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int):
    try:
        return ServiceOut.from_orm(Service.objects.get(pk=service_id))
    except Service.DoesNotExist:
        raise HTTPException(status_code=404, detail="Service not found")

@router.patch("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, service_in: ServiceUpdate):
    try:
        service = Service.objects.get(pk=service_id)
        update_data = service_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service, field, value)
        service.save()
        return ServiceOut.from_orm(service)
    except Service.DoesNotExist:
        raise HTTPException(status_code=404, detail="Service not found")

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int):
    try:
        Service.objects.get(pk=service_id).delete()
        return None
    except Service.DoesNotExist:
        raise HTTPException(status_code=404, detail="Service not found")
