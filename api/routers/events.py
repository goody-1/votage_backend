from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from apps.events.models import Event, EventParticipation
from ..schemas.events import EventCreate, EventUpdate, EventOut, EventParticipationCreate, EventParticipationOut
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/events",
    tags=["Events"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=List[EventOut])
def list_events():
    return [EventOut.from_orm(e) for e in Event.objects.all()]

@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(event_in: EventCreate):
    event = Event.objects.create(**event_in.dict())
    return EventOut.from_orm(event)

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int):
    try:
        return EventOut.from_orm(Event.objects.get(pk=event_id))
    except Event.DoesNotExist:
        raise HTTPException(status_code=404, detail="Event not found")

@router.patch("/{event_id}", response_model=EventOut)
def update_event(event_id: int, event_in: EventUpdate):
    try:
        event = Event.objects.get(pk=event_id)
        update_data = event_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)
        event.save()
        return EventOut.from_orm(event)
    except Event.DoesNotExist:
        raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int):
    try:
        Event.objects.get(pk=event_id).delete()
        return None
    except Event.DoesNotExist:
        raise HTTPException(status_code=404, detail="Event not found")

# Participation
@router.get("/{event_id}/participants/", response_model=List[EventParticipationOut])
def list_participants(event_id: int):
    return [EventParticipationOut.from_orm(p) for p in EventParticipation.objects.filter(event_id=event_id)]

@router.post("/participation/", response_model=EventParticipationOut, status_code=status.HTTP_201_CREATED)
def add_participant(p_in: EventParticipationCreate):
    p = EventParticipation.objects.create(**p_in.dict())
    return EventParticipationOut.from_orm(p)
