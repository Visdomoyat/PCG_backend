from django import forms
from django.contrib.auth.models import User

from .models import GalleryItem, SiteContent, Story


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ["name", "media_type", "file", "sort_order", "is_published"]
        labels = {
            "name": "Display name",
            "media_type": "Media type",
            "file": "Image or video file",
            "sort_order": "Display order (lower shows first)",
            "is_published": "Publish to public frontend",
        }
        help_texts = {
            "name": "Shown in the admin list and returned by the public gallery API.",
            "media_type": "Choose image or video before uploading so the file is validated correctly.",
            "file": "Images: jpg, png, webp, gif, HEIC/HEIF. Videos: mp4, mov, webm. Note: some browsers do not display HEIC in img tags—convert to JPEG/PNG for universal web display.",
            "is_published": "When on, this item is included in GET /api/gallery/ for anonymous users.",
        }
        widgets = {
            "media_type": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["file"].required = False
            self.fields["file"].help_text = "Upload a new file to replace the current one. Leave empty to keep the existing file."


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            "title",
            "excerpt",
            "body",
            "cover_image",
            "sort_order",
            "is_published",
        ]
        labels = {
            "title": "Story Title",
            "excerpt": "Excerpt (short preview for cards and SEO)",
            "body": "Full Story",
            "cover_image": "Cover Image",
            "sort_order": "Display Order (lower shows first)",
            "is_published": "Publish to Public Frontend",
        }
        help_texts = {
            "is_published": "When on, this story is returned by the public stories API for your read-only site.",
        }
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 12}),
        }

class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent
        fields = [
            "title",
            "personal_title",
            "personal_bio",
            "professional_title",
            "professional_bio",
            "is_active",
            "is_published",
        ]
        labels = {
            "title": "Entry Title",
            "personal_title": "Personal Bio Title",
            "professional_title": "Professional Bio Title",
            "is_published": "Publish to Public Frontend",
        }
        help_texts = {
            "is_active": "When off, this entry is treated as inactive in legacy admin/API filters.",
            "is_published": "When on, this entry is included in the public read-only site API.",
        }


class AdminAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {"username": "Admin Username"}
