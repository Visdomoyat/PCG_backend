from rest_framework import serializers

from .models import SiteContent


class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = [
            "id",
            "title",
            "slug",
            "personal_title",
            "personal_bio",
            "professional_title",
            "professional_bio",
            "is_published",
            "updated_at",
        ]
