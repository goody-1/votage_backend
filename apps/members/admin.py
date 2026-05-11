from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Member
from ..connect_groups.models import ConnectGroupMember
from ..growth_track.models import GrowthTrackEnrollment


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'email',
        'gender',
        'member_status',
        'date_joined',
    )
    list_filter = ('member_status', 'gender', 'date_joined')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    # readonly_fields = ('date_joined',)
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('first_name', 'last_name'),
                ('phone', 'email'),
                ('birthday', 'gender'),
                'member_status',
            )
        }),
        ('Membership Dates', {
            'fields': ('date_joined',)
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    ordering = ('-date_joined', 'last_name', 'first_name')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Name"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()  # optimize if needed


@admin.register(ConnectGroupMember)
class ConnectGroupMemberAdmin(admin.ModelAdmin):
    list_display = (
        'member_link',
        'connect_group',
        'joined_at',
        'left_at',
        'is_active',
    )
    list_filter = ('connect_group', 'joined_at', 'left_at')
    search_fields = (
        'member__first_name',
        'member__last_name',
        'member__phone',
        'connect_group__name',
    )
    raw_id_fields = ('member',)
    autocomplete_fields = ['member']
    date_hierarchy = 'joined_at'
    ordering = ('-joined_at',)

    def member_link(self, obj):
        url = f"/admin/members/member/{obj.member.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.member)
    member_link.short_description = "Member"

    def is_active(self, obj):
        return obj.left_at is None
    is_active.boolean = True
    is_active.short_description = "Active"


# @admin.register(GrowthTrackEnrollment)
# class GrowthTrackEnrollmentAdmin(admin.ModelAdmin):
#     list_display = (
#         'member',
#         'growth_track',
#         'enrollment_date',
#         'status',
#         'graduation_date',
#     )
#     list_filter = ('status', 'growth_track', 'enrollment_date')
#     search_fields = (
#         'member__first_name',
#         'member__last_name',
#         'growth_track__cohort_name',
#     )
#     raw_id_fields = ('member',)
#     autocomplete_fields = ['member']
#     date_hierarchy = 'enrollment_date'
#     readonly_fields = ('enrollment_date',)
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'growth_track',
#                 'member',
#                 'enrollment_date',
#                 'status',
#                 'graduation_date',
#             )
#         }),
#     )
