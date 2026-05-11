from fastapi import APIRouter, Depends
from apps.members.models import Member
from apps.attendance.models import Attendance
from apps.growth_track.models import GrowthTrack
from apps.events.models import Event
from apps.departments.models import Department
from ..schemas.dashboard import DashboardStats, DashboardSummary, ChartDataPoint
from ..schemas.members import MemberOut
from ..schemas.events import EventOut
from ..deps import get_current_admin_user
from django.utils import timezone

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    today = timezone.now().date()
    from django.db.models import Count, Max, Avg, Q
    from django.db.models.functions import TruncMonth
    
    total_count = Member.objects.count()
    active_count = total_count # Assuming all are active since no status field exists
    
    # Returning members
    returning_count = Attendance.objects.values('member').annotate(total=Count('id')).filter(total__gt=1).count()
    
    # Engagement rate (30 days)
    last_30_days = today - timezone.timedelta(days=30)
    attended_recently = Attendance.objects.filter(service_date__gte=last_30_days).values('member').distinct().count()
    engagement_rate = round((attended_recently / total_count * 100), 1) if total_count > 0 else 0.0

    # Weekly Avg & Peak (last 6 months)
    service_attendance = Attendance.objects.values('service_date').annotate(count=Count('id'))
    peak_attendance = service_attendance.aggregate(Max('count'))['count__max'] or 0
    avg_weekly = service_attendance.aggregate(Avg('count'))['count__avg'] or 0.0

    # Year-over-Year Growth
    one_year_ago = today - timezone.timedelta(days=365)
    members_last_year = Member.objects.filter(date_joined__lte=one_year_ago).count()
    yoy_growth = round(((total_count - members_last_year) / members_last_year * 100), 1) if members_last_year > 0 else 0.0

    try:
        growth_tracks_ongoing = GrowthTrack.objects.filter(status="ongoing").count()
    except Exception:
        growth_tracks_ongoing = 0
        
    try:
        upcoming_events_count = Event.objects.filter(service__service_date__gte=today).count()
    except Exception:
        upcoming_events_count = 0
        
    try:
        departments_count = Department.objects.count()
    except Exception:
        departments_count = 0

    stats = DashboardStats(
        total_members=total_count,
        active_members=active_count,
        returning_members=returning_count,
        engagement_rate=engagement_rate,
        avg_weekly_attendance=round(avg_weekly, 1),
        peak_attendance=peak_attendance,
        yoy_growth_rate=yoy_growth,
        growth_tracks_ongoing=growth_tracks_ongoing,
        upcoming_events_count=upcoming_events_count,
        departments_count=departments_count
    )
    
    # Chart Data: Attendance (Last 6 Months)
    attendance_trends = (
        Attendance.objects.filter(service_date__gte=today - timezone.timedelta(days=180))
        .annotate(month=TruncMonth('service_date'))
        .values('month')
        .annotate(value=Count('id'))
        .order_by('month')
    )
    attendance_chart = [
        ChartDataPoint(label=item['month'].strftime("%b"), value=float(item['value']))
        for item in attendance_trends
    ]

    # Chart Data: Member Growth (Last 6 Months)
    member_trends = (
        Member.objects.filter(date_joined__gte=today - timezone.timedelta(days=180))
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(value=Count('id'))
        .order_by('month')
    )
    member_growth_chart = [
        ChartDataPoint(label=item['month'].strftime("%b"), value=float(item['value']))
        for item in member_trends
    ]

    recent_members = [MemberOut.from_orm(m) for m in Member.objects.all().order_by("-id")[:5]]
    try:
        upcoming_events = [EventOut.from_orm(e) for e in Event.objects.filter(service__service_date__gte=today).order_by("service__service_date")[:5]]
    except Exception:
        upcoming_events = []
    
    return DashboardSummary(
        stats=stats,
        recent_members=recent_members,
        upcoming_events=upcoming_events,
        attendance_chart=attendance_chart,
        member_growth_chart=member_growth_chart
    )
