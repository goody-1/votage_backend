from typing import List, Optional
from pydantic import BaseModel
from .members import MemberOut
from .events import EventOut

class ChartDataPoint(BaseModel):
    label: str  # e.g., "Jan", "Feb" or "Week 1"
    value: float

class DashboardStats(BaseModel):
    total_members: int
    active_members: int
    returning_members: int
    engagement_rate: float
    avg_weekly_attendance: float
    peak_attendance: int
    yoy_growth_rate: float
    growth_tracks_ongoing: int
    upcoming_events_count: int
    departments_count: int

class DashboardSummary(BaseModel):
    stats: DashboardStats
    recent_members: List[MemberOut]
    upcoming_events: List[EventOut]
    attendance_chart: List[ChartDataPoint]
    member_growth_chart: List[ChartDataPoint]
