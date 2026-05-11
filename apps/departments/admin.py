# apps/departments/admin.py
from django.contrib import admin
from .models import (
    Directorate,
    Department,
    DepartmentMembership,
    Unit,
    UnitMembership,
)

# Inline for Departments inside Directorate
class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1                  # how many empty rows to show by default
    fields = ('name', 'hod', 'assistant_hod', 'description')
    show_change_link = True    # adds a link to edit the full Department page


# Inline for Units inside Department
class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1
    fields = ('name', 'unit_head', 'description')
    show_change_link = True


# Inline for DepartmentMembership inside Department (shows members directly)
class DepartmentMembershipInline(admin.TabularInline):
    model = DepartmentMembership
    extra = 1
    fields = ('member', 'joined_at', 'is_active')
    raw_id_fields = ('member',)   # better for large Member querysets (shows search popup)
    autocomplete_fields = ['member']  # if you set up search_fields on Member admin


# Inline for UnitMembership inside Unit
class UnitMembershipInline(admin.TabularInline):
    model = UnitMembership
    extra = 1
    fields = ('member', 'joined_at', 'is_active', 'role')
    raw_id_fields = ('member',)
    autocomplete_fields = ['member']

@admin.register(Directorate)
class DirectorateAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'director__first_name', 'director__last_name')
    inlines = [DepartmentInline]               # ← see/add departments here
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'directorate', 'hod', 'assistant_hod', 'created_at')
    list_filter = ('directorate', 'created_at')
    search_fields = ('name', 'description', 'hod__first_name', 'hod__last_name')
    inlines = [
        UnitInline,                     # ← see/add units here
        DepartmentMembershipInline,     # ← see/add direct department members
    ]
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'unit_head', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('name', 'description', 'unit_head__first_name', 'unit_head__last_name')
    inlines = [UnitMembershipInline]           # ← see/add unit members here
@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'department', 'joined_at', 'is_active')
    list_filter = ('is_active', 'department', 'joined_at')
    search_fields = ('member__first_name', 'member__last_name', 'department__name')
    raw_id_fields = ('member', 'department')
    autocomplete_fields = ['member', 'department']
@admin.register(UnitMembership)
class UnitMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'unit', 'joined_at', 'is_active', 'role')
    list_filter = ('is_active', 'unit__department', 'joined_at')
    search_fields = ('member__first_name', 'member__last_name', 'unit__name', 'role')
    raw_id_fields = ('member', 'unit')
    autocomplete_fields = ['member', 'unit']



# admin.site.register(Directorate)
# admin.site.register(Department)
# admin.site.register(Unit)
# admin.site.register(DepartmentMembership)
# admin.site.register(UnitMembership)
