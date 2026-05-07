import json

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import AdminAccountForm, SiteContentForm
from .models import SiteContent, Story, Testimonial


def _is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(_is_staff)
def content_landing(request):
    return render(request, "landing.html")


@login_required
@user_passes_test(_is_staff)
def content_admin(request):
    entries = SiteContent.objects.order_by("-updated_at")
    form = SiteContentForm()
    return render(
        request,
        "contentAdmin.html",
        {
            "entries": entries,
            "form": form,
            "editing_entry": None,
        },
    )


@login_required
@user_passes_test(_is_staff)
def create_site_content(request):
    if request.method != "POST":
        return redirect("contentAdmin")
    form = SiteContentForm(request.POST)
    if form.is_valid():
        content = form.save(commit=False)
        content.updated_by = request.user
        content.save()
        messages.success(request, "Content entry created.")
    else:
        messages.error(request, "Unable to create entry. Please fix the form errors.")
    return redirect("contentAdmin")


@login_required
@user_passes_test(_is_staff)
def edit_site_content(request, slug):
    entry = get_object_or_404(SiteContent, slug=slug)
    if request.method == "POST":
        form = SiteContentForm(request.POST, instance=entry)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_by = request.user
            updated.save()
            messages.success(request, "Content entry updated.")
            return redirect("contentAdmin")
        messages.error(request, "Unable to update entry. Please fix the form errors.")
    else:
        form = SiteContentForm(instance=entry)
    entries = SiteContent.objects.order_by("-updated_at")
    return render(
        request,
        "contentAdmin.html",
        {
            "entries": entries,
            "form": form,
            "editing_entry": entry,
        },
    )


@login_required
@user_passes_test(_is_staff)
def delete_site_content(request, slug):
    entry = get_object_or_404(SiteContent, slug=slug)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Content entry deleted.")
    return redirect("contentAdmin")


@login_required
@user_passes_test(_is_staff)
def CRMAdmin(request):
    return render(request, "CRMAdmin.html")


@login_required
@user_passes_test(_is_staff)
def stories_page(request):
    return render(request, "stories.html")


@login_required
@user_passes_test(_is_staff)
def account_settings(request):
    username_form = AdminAccountForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "username":
            username_form = AdminAccountForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Admin username updated.")
                return redirect("accountSettings")
            messages.error(request, "Unable to update username. Please check the form.")
        elif form_type == "password":
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully.")
                return redirect("accountSettings")
            messages.error(request, "Unable to update password. Please check the form.")

    return render(
        request,
        "account_settings.html",
        {
            "username_form": username_form,
            "password_form": password_form,
        },
    )


def _to_bool(value):
    return str(value).lower() in {"1", "true", "yes"}


def _parse_json_body(request):
    try:
        if not request.body:
            return {}
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _require_staff(request):
    return request.user.is_authenticated and request.user.is_staff


def _site_content_to_dict(entry):
    return {
        "id": entry.id,
        "title": entry.title,
        "slug": entry.slug,
        "personal_title": entry.personal_title,
        "personal_bio": entry.personal_bio,
        "professional_title": entry.professional_title,
        "professional_bio": entry.professional_bio,
        "is_active": entry.is_active,
        "updated_at": entry.updated_at.isoformat(),
        "updated_by": entry.updated_by.username if entry.updated_by else None,
    }


def _story_to_dict(story):
    return {
        "id": story.id,
        "title": story.title,
        "slug": story.slug,
        "excerpt": story.excerpt,
        "body": story.body,
        "cover_image": story.cover_image.url if story.cover_image else None,
        "is_published": story.is_published,
        "published_at": story.published_at.isoformat() if story.published_at else None,
        "sort_order": story.sort_order,
        "created_at": story.created_at.isoformat(),
        "updated_at": story.updated_at.isoformat(),
        "updated_by": story.updated_by.username if story.updated_by else None,
    }


def _testimonial_to_dict(item):
    return {
        "id": item.id,
        "customer_name": item.customer_name,
        "customer_email": item.customer_email,
        "company": item.company,
        "rating": item.rating,
        "headline": item.headline,
        "body": item.body,
        "status": item.status,
        "submitted_at": item.submitted_at.isoformat(),
        "reviewed_at": item.reviewed_at.isoformat() if item.reviewed_at else None,
        "reviewed_by": item.reviewed_by.username if item.reviewed_by else None,
        "is_featured": item.is_featured,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def about_collection_api(request):
    if request.method == "GET":
        queryset = SiteContent.objects.order_by("-updated_at")
        if not _require_staff(request):
            queryset = queryset.filter(is_active=True)
        return JsonResponse({"results": [_site_content_to_dict(item) for item in queryset]})

    if not _require_staff(request):
        return JsonResponse({"detail": "Admin authentication required."}, status=403)
    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    title = data.get("title")
    personal_bio = data.get("personal_bio")
    professional_bio = data.get("professional_bio")
    if not title or not personal_bio or not professional_bio:
        return JsonResponse(
            {"detail": "title, personal_bio, and professional_bio are required."},
            status=400,
        )

    entry = SiteContent(
        title=title,
        personal_title=data.get("personal_title", "Personal Biography"),
        personal_bio=personal_bio,
        professional_title=data.get("professional_title", "Professional Biography"),
        professional_bio=professional_bio,
        is_active=_to_bool(data.get("is_active", True)),
        updated_by=request.user,
    )
    entry.save()
    return JsonResponse(_site_content_to_dict(entry), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def about_detail_api(request, slug):
    entry = get_object_or_404(SiteContent, slug=slug)

    if request.method == "GET":
        if not entry.is_active and not _require_staff(request):
            return JsonResponse({"detail": "Not found."}, status=404)
        return JsonResponse(_site_content_to_dict(entry))

    if not _require_staff(request):
        return JsonResponse({"detail": "Admin authentication required."}, status=403)

    if request.method in {"PUT", "PATCH"}:
        data = _parse_json_body(request)
        if data is None:
            return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

        for field in [
            "title",
            "personal_title",
            "personal_bio",
            "professional_title",
            "professional_bio",
        ]:
            if field in data:
                setattr(entry, field, data[field])
        if "is_active" in data:
            entry.is_active = _to_bool(data["is_active"])
        entry.updated_by = request.user
        entry.save()
        return JsonResponse(_site_content_to_dict(entry))

    entry.delete()
    return JsonResponse({}, status=204)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def stories_collection_api(request):
    if request.method == "GET":
        queryset = Story.objects.order_by("sort_order", "-published_at", "-created_at")
        if not _require_staff(request):
            queryset = queryset.filter(is_published=True)
        return JsonResponse({"results": [_story_to_dict(item) for item in queryset]})

    if not _require_staff(request):
        return JsonResponse({"detail": "Admin authentication required."}, status=403)
    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    title = data.get("title")
    if not title:
        return JsonResponse({"detail": "title is required."}, status=400)

    story = Story(
        title=title,
        excerpt=data.get("excerpt", ""),
        body=data.get("body", ""),
        is_published=_to_bool(data.get("is_published", False)),
        sort_order=data.get("sort_order", 0) or 0,
        updated_by=request.user,
    )
    story.save()
    return JsonResponse(_story_to_dict(story), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def story_detail_api(request, slug):
    story = get_object_or_404(Story, slug=slug)

    if request.method == "GET":
        if not story.is_published and not _require_staff(request):
            return JsonResponse({"detail": "Not found."}, status=404)
        return JsonResponse(_story_to_dict(story))

    if not _require_staff(request):
        return JsonResponse({"detail": "Admin authentication required."}, status=403)

    if request.method in {"PUT", "PATCH"}:
        data = _parse_json_body(request)
        if data is None:
            return JsonResponse({"detail": "Invalid JSON payload."}, status=400)
        for field in ["title", "excerpt", "body"]:
            if field in data:
                setattr(story, field, data[field])
        if "is_published" in data:
            story.is_published = _to_bool(data["is_published"])
        if "sort_order" in data:
            story.sort_order = data["sort_order"] or 0
        story.updated_by = request.user
        story.save()
        return JsonResponse(_story_to_dict(story))

    story.delete()
    return JsonResponse({}, status=204)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def testimonials_collection_api(request):
    if request.method == "GET":
        queryset = Testimonial.objects.order_by("-submitted_at")
        if not _require_staff(request):
            queryset = queryset.filter(status=Testimonial.Status.APPROVED)
        return JsonResponse({"results": [_testimonial_to_dict(item) for item in queryset]})

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    required_fields = ["customer_name", "customer_email", "headline", "body"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return JsonResponse({"detail": f"Missing required fields: {', '.join(missing)}."}, status=400)

    testimonial = Testimonial(
        customer_name=data["customer_name"],
        customer_email=data["customer_email"],
        company=data.get("company", ""),
        rating=data.get("rating", 5) or 5,
        headline=data["headline"],
        body=data["body"],
        status=Testimonial.Status.PENDING,
        is_featured=False,
    )
    try:
        testimonial.full_clean()
    except ValidationError as exc:
        return JsonResponse({"detail": exc.message_dict if hasattr(exc, "message_dict") else exc.messages}, status=400)
    testimonial.save()
    return JsonResponse(_testimonial_to_dict(testimonial), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def testimonial_detail_api(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)

    if request.method == "GET":
        if testimonial.status != Testimonial.Status.APPROVED and not _require_staff(request):
            return JsonResponse({"detail": "Not found."}, status=404)
        return JsonResponse(_testimonial_to_dict(testimonial))

    if not _require_staff(request):
        return JsonResponse({"detail": "Admin authentication required."}, status=403)

    if request.method in {"PUT", "PATCH"}:
        data = _parse_json_body(request)
        if data is None:
            return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

        for field in ["customer_name", "customer_email", "company", "headline", "body"]:
            if field in data:
                setattr(testimonial, field, data[field])
        if "rating" in data:
            testimonial.rating = data["rating"]
        if "is_featured" in data:
            testimonial.is_featured = _to_bool(data["is_featured"])
        if "status" in data:
            new_status = data["status"]
            if new_status not in Testimonial.Status.values:
                return JsonResponse({"detail": "Invalid status."}, status=400)
            testimonial.mark_reviewed(request.user, new_status)
        try:
            testimonial.full_clean()
        except ValidationError as exc:
            return JsonResponse({"detail": exc.message_dict if hasattr(exc, "message_dict") else exc.messages}, status=400)
        testimonial.save()
        return JsonResponse(_testimonial_to_dict(testimonial))

    testimonial.delete()
    return JsonResponse({}, status=204)
