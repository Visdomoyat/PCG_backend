from django import forms
from django.contrib.auth.models import User

from .models import SiteContent, Story


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
