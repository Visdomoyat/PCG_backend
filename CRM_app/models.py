# crm/models.py
from django.db import models

class Lead(models.Model):
    class Source(models.TextChoices):
        WEBSITE = "website", "Website"
        INSTAGRAM = "instagram", "Instagram"
        REFERRAL = "referral", "Referral"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        PROPOSAL_SENT = "proposal_sent", "Proposal Sent"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)

    event_type = models.CharField(max_length=120, blank=True)
    event_date = models.DateField(blank=True, null=True)
    guest_count = models.PositiveIntegerField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    message = models.TextField(blank=True)
    source = models.CharField(max_length=30, choices=Source.choices, default=Source.WEBSITE)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    priority = models.PositiveSmallIntegerField(default=3)  # 1 high, 5 low

    owner = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="owned_leads"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["priority", "-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    created_by = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note for {self.lead_id}"
# Create your models here.
class LeadTask(models.Model):
    class TaskStatus(models.TextChoices):
        OPEN = "open", "Open"
        DONE = "done", "Done"
        CANCELED = "canceled", "Canceled"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    due_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.OPEN)

    assigned_to = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="lead_tasks"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["status", "due_at", "-created_at"]

    def __str__(self):
        return self.title
