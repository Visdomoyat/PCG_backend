from django.contrib import admin
from .models import SiteContent, Story, StoryMedia, Testimonial, TestimonialAsset

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "is_published", "updated_at", "updated_by")
    search_fields = ("title", "personal_bio", "professional_bio")


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "updated_at", "updated_by")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "body")


@admin.register(StoryMedia)
class StoryMediaAdmin(admin.ModelAdmin):
    list_display = ("story", "media_type", "uploaded_at")
    list_filter = ("media_type",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "customer_email",
        "rating",
        "status",
        "is_featured",
        "submitted_at",
        "reviewed_by",
    )
    list_filter = ("status", "is_featured", "rating")
    search_fields = ("customer_name", "customer_email", "headline", "body")


@admin.register(TestimonialAsset)
class TestimonialAssetAdmin(admin.ModelAdmin):
    list_display = ("testimonial", "asset_type", "uploaded_at")
    list_filter = ("asset_type",)
