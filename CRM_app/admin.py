from django.contrib import admin

from .models import Lead, LeadNote, LeadTask, Service


class LeadNoteInline(admin.TabularInline):
    model = LeadNote
    extra = 0
    readonly_fields = ("created_at", "created_by")


class LeadTaskInline(admin.TabularInline):
    model = LeadTask
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "email",
        "status",
        "source",
        "priority",
        "event_date",
        "owner",
        "created_at",
    )
    list_filter = ("status", "source", "priority")
    search_fields = ("first_name", "last_name", "email", "phone", "message")
    filter_horizontal = ("services",)
    inlines = [LeadNoteInline, LeadTaskInline]


@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = ("lead", "created_by", "created_at")
    search_fields = ("note",)


@admin.register(LeadTask)
class LeadTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "lead", "status", "due_at", "assigned_to")
    list_filter = ("status",)
