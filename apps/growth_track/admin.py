from django.contrib import admin

from django.utils.html import format_html
from .models import GrowthTrack, GrowthTrackEnrollment

# Register your models here.


@admin.register(GrowthTrack)
class GrowthTrackAdmin(admin.ModelAdmin):
    list_display = [
        "cohort_name",
        "start_date",
        "end_date",
        "status_colored",
        "enrollment_count",
        "created_at",
    ]
    list_filter = ["status", "start_date", "end_date"]
    search_fields = ["cohort_name"]
    ordering = ["-start_date"]
    date_hierarchy = "start_date"
    list_per_page = 20

    fieldsets = (
        (None, {
            "fields": ("cohort_name", "status")
        }),
        ("Dates", {
            "fields": ("start_date", "end_date"),
            "classes": ("grp-collapse grp-open",),
        }),
        ("Extra", {
            "fields": ("created_at",),
            "classes": ("grp-collapse grp-closed",),
        }),
    )

    readonly_fields = ["created_at"]

    def status_colored(self, obj):
        colors = {
            "planned": "orange",
            "ongoing": "green",
            "completed": "blue",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "Status"

    def enrollment_count(self, obj):
        count = obj.growthtrackenrollment_set.count()
        return count
    enrollment_count.short_description = "Enrollments"


@admin.register(GrowthTrackEnrollment)
class GrowthTrackEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        "member_link",
        "growth_track",
        "enrollment_date",
        "status_colored",
        "graduation_date",
    ]
    list_filter = [
        "status",
        "growth_track",
        "enrollment_date",
        "graduation_date",
    ]
    search_fields = [
        "member__first_name",
        "member__last_name",
        "member__email",
        "growth_track__cohort_name",
    ]
    raw_id_fields = ["member", "growth_track"]   # better for large datasets
    date_hierarchy = "enrollment_date"
    ordering = ["-enrollment_date"]
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("growth_track", "member", "status")
        }),
        ("Dates", {
            "fields": ("enrollment_date", "graduation_date"),
        }),
    )

    def member_link(self, obj):
        url = f"/admin/members/member/{obj.member_id}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            str(obj.member)
        )
    member_link.short_description = "Member"

    def status_colored(self, obj):
        colors = {
            "active": "green",
            "completed": "blue",
            "dropped": "red",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "Status"


# Optional: Inline version if you prefer to see enrollments directly on GrowthTrack page

# class GrowthTrackEnrollmentInline(admin.TabularInline):
#     model = GrowthTrackEnrollment
#     extra = 0
#     raw_id_fields = ["member"]
#     fields = ["member", "enrollment_date", "status", "graduation_date"]
#     readonly_fields = ["enrollment_date"]   # optional

#     def has_add_permission(self, request, obj=None):
#         return True   # or False if you want to restrict adding from here

# Uncomment to use inline on GrowthTrack page:
# GrowthTrackAdmin.inlines = [GrowthTrackEnrollmentInline]
