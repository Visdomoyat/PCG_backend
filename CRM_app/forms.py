from django import forms
from django.contrib.auth import get_user_model

from .models import Lead, LeadNote, LeadTask, Service

User = get_user_model()


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "is_active", "sort_order"]
        labels = {
            "name": "Service name",
            "sort_order": "Display order (lower first)",
            "is_active": "Available to assign to leads",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "event_type",
            "event_date",
            "guest_count",
            "budget",
            "message",
            "source",
            "status",
            "priority",
            "services",
            "owner",
            "contacted_at",
        ]
        labels = {
            "event_type": "Event / inquiry type",
            "priority": "Priority (1 = highest, 5 = lowest)",
            "contacted_at": "First contacted at",
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
            "services": forms.CheckboxSelectMultiple,
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "contacted_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["services"].queryset = Service.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        )
        self.fields["owner"].queryset = User.objects.filter(is_staff=True).order_by("username")
        self.fields["owner"].required = False


class LeadNoteForm(forms.ModelForm):
    class Meta:
        model = LeadNote
        fields = ["note"]
        labels = {"note": "Add a note"}
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3, "placeholder": "e.g. Called 5/21 — wants vegan menu"}),
        }


class LeadTaskForm(forms.ModelForm):
    class Meta:
        model = LeadTask
        fields = ["title", "due_at", "assigned_to"]
        labels = {
            "title": "Task",
            "due_at": "Due date & time",
        }
        widgets = {
            "due_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = User.objects.filter(is_staff=True).order_by("username")
        self.fields["assigned_to"].required = False
