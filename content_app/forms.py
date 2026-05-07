from django import forms
from django.contrib.auth.models import User

from .models import SiteContent


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
        ]
        labels = {
            "title": "Entry Title",
            "personal_title": "Personal Bio Title",
            "professional_title": "Professional Bio Title",
        }


class AdminAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {"username": "Admin Username"}
