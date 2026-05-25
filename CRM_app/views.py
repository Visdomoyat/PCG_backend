from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LeadForm, LeadNoteForm, LeadTaskForm, ServiceForm
from .models import Lead, LeadNote, LeadTask, Service


def _is_staff(user):
    return user.is_staff


def _leads_queryset(status_filter=None):
    qs = Lead.objects.prefetch_related("services", "notes", "tasks")
    if status_filter and status_filter in Lead.Status.values:
        qs = qs.filter(status=status_filter)
    return qs


@login_required
@user_passes_test(_is_staff)
def crm_home(request):
    status_filter = request.GET.get("status", "").strip()
    leads = _leads_queryset(status_filter or None)
    status_tabs = [{"value": "", "label": "All", "count": Lead.objects.count()}]
    for value, label in Lead.Status.choices:
        status_tabs.append(
            {"value": value, "label": label, "count": Lead.objects.filter(status=value).count()}
        )
    return render(
        request,
        "crm/leads_list.html",
        {
            "leads": leads,
            "status_filter": status_filter,
            "status_tabs": status_tabs,
            "lead_form": LeadForm(),
        },
    )


@login_required
@user_passes_test(_is_staff)
def create_lead(request):
    if request.method != "POST":
        return redirect("CRMAdmin")
    form = LeadForm(request.POST)
    if form.is_valid():
        lead = form.save()
        messages.success(request, f"Lead created for {lead.display_name}.")
        return redirect("editLead", pk=lead.pk)
    messages.error(request, "Unable to create lead. Please fix the form errors.")
    status_filter = request.GET.get("status", "").strip()
    status_tabs = [{"value": "", "label": "All", "count": Lead.objects.count()}]
    for value, label in Lead.Status.choices:
        status_tabs.append(
            {"value": value, "label": label, "count": Lead.objects.filter(status=value).count()}
        )
    return render(
        request,
        "crm/leads_list.html",
        {
            "leads": _leads_queryset(status_filter or None),
            "status_filter": status_filter,
            "status_tabs": status_tabs,
            "lead_form": form,
            "show_create_form": True,
        },
    )


@login_required
@user_passes_test(_is_staff)
def edit_lead(request, pk):
    lead = get_object_or_404(Lead.objects.prefetch_related("services", "notes", "tasks"), pk=pk)

    if request.method == "POST":
        form_type = request.POST.get("form_type", "lead")
        if form_type == "lead":
            form = LeadForm(request.POST, instance=lead)
            if form.is_valid():
                updated = form.save()
                if updated.status == Lead.Status.CONTACTED and not updated.contacted_at:
                    updated.contacted_at = timezone.now()
                    updated.save(update_fields=["contacted_at"])
                messages.success(request, "Lead updated.")
                return redirect("editLead", pk=lead.pk)
            note_form = LeadNoteForm()
            task_form = LeadTaskForm()
        elif form_type == "note":
            note_form = LeadNoteForm(request.POST)
            form = LeadForm(instance=lead)
            task_form = LeadTaskForm()
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.lead = lead
                note.created_by = request.user
                note.save()
                messages.success(request, "Note added.")
                return redirect("editLead", pk=lead.pk)
            messages.error(request, "Unable to add note.")
        elif form_type == "task":
            task_form = LeadTaskForm(request.POST)
            form = LeadForm(instance=lead)
            note_form = LeadNoteForm()
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.lead = lead
                if not task.assigned_to:
                    task.assigned_to = request.user
                task.save()
                messages.success(request, "Task added.")
                return redirect("editLead", pk=lead.pk)
            messages.error(request, "Unable to add task.")
        else:
            form = LeadForm(instance=lead)
            note_form = LeadNoteForm()
            task_form = LeadTaskForm()
    else:
        form = LeadForm(instance=lead)
        note_form = LeadNoteForm()
        task_form = LeadTaskForm()

    return render(
        request,
        "crm/lead_detail.html",
        {
            "lead": lead,
            "form": form,
            "note_form": note_form,
            "task_form": task_form,
        },
    )


@login_required
@user_passes_test(_is_staff)
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        name = lead.display_name
        lead.delete()
        messages.success(request, f"Deleted lead for {name}.")
    return redirect("CRMAdmin")


@login_required
@user_passes_test(_is_staff)
def update_task_status(request, pk, task_id):
    if request.method != "POST":
        return redirect("editLead", pk=pk)
    lead = get_object_or_404(Lead, pk=pk)
    task = get_object_or_404(LeadTask, pk=task_id, lead=lead)
    new_status = request.POST.get("status")
    if new_status in LeadTask.TaskStatus.values:
        task.status = new_status
        task.save(update_fields=["status"])
        messages.success(request, "Task updated.")
    return redirect("editLead", pk=pk)


@login_required
@user_passes_test(_is_staff)
def delete_task(request, pk, task_id):
    if request.method == "POST":
        task = get_object_or_404(LeadTask, pk=task_id, lead_id=pk)
        task.delete()
        messages.success(request, "Task removed.")
    return redirect("editLead", pk=pk)


@login_required
@user_passes_test(_is_staff)
def services_page(request):
    services = Service.objects.order_by("sort_order", "name")
    form = ServiceForm()
    editing = None
    edit_id = request.GET.get("edit")
    if edit_id and edit_id.isdigit():
        editing = Service.objects.filter(pk=int(edit_id)).first()

    if request.method == "POST":
        service_id = request.POST.get("service_id")
        instance = Service.objects.filter(pk=service_id).first() if service_id else None
        form = ServiceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Service saved.")
            return redirect("crmServices")
        messages.error(request, "Unable to save service.")
        editing = instance

    if editing and request.method != "POST":
        form = ServiceForm(instance=editing)

    return render(
        request,
        "crm/services.html",
        {
            "services": services,
            "form": form,
            "editing_service": editing,
        },
    )


@login_required
@user_passes_test(_is_staff)
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        name = service.name
        service.delete()
        messages.success(request, f"Deleted service “{name}”.")
    return redirect("crmServices")
