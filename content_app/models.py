from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User
MAX_VIDEO_BYTES = 60 * 1024 * 1024  # 60MB


def validate_video_file(file):
    allowed = [".mp4", ".mov", ".webm"]
    name = file.name.lower()
    if not any(name.endswith(ext) for ext in allowed):
        raise ValidationError("Unsupported video format. Use mp4, mov, or webm.")
    if file.size > MAX_VIDEO_BYTES:
        raise ValidationError("Video is too large.")


class SiteContent(models.Model):
    title = models.CharField(max_length=200, default="Global Site Content")
    personal_title = models.CharField(max_length=200, default="Personal Biography")
    personal_bio = models.TextField()
    professional_title = models.CharField(max_length=200, default="Professional Biography")
    professional_bio = models.TextField()
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_site_content",
    )

    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"

    def _generate_unique_slug(self):
        base_slug = slugify(self.title) or "site-content"
        slug_candidate = base_slug
        suffix = 2
        while SiteContent.objects.exclude(pk=self.pk).filter(slug=slug_candidate).exists():
            slug_candidate = f"{base_slug}-{suffix}"
            suffix += 1
        return slug_candidate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Story(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220, blank=True)
    excerpt = models.CharField(max_length=320, blank=True)
    body = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="stories/", blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_stories",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-published_at", "-created_at"]

    def _generate_unique_slug(self):
        base_slug = slugify(self.title) or "story"
        slug_candidate = base_slug
        suffix = 2
        while Story.objects.exclude(pk=self.pk).filter(slug=slug_candidate).exists():
            slug_candidate = f"{base_slug}-{suffix}"
            suffix += 1
        return slug_candidate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class StoryMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    file = models.FileField(upload_to="stories/media/")
    caption = models.CharField(max_length=280, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]

    def clean(self):
        super().clean()
        if not self.file:
            return
        if self.media_type == self.MediaType.VIDEO:
            validate_video_file(self.file)
        elif self.media_type == self.MediaType.IMAGE:
            allowed = [".jpg", ".jpeg", ".png", ".webp"]
            if not any(self.file.name.lower().endswith(ext) for ext in allowed):
                raise ValidationError("Unsupported image format.")

    def __str__(self):
        return f"{self.story.title} - {self.media_type} ({self.file.name})"


class Testimonial(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    headline = models.CharField(max_length=200)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_testimonials",
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def clean(self):
        super().clean()
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    def mark_reviewed(self, reviewer, status):
        self.status = status
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()

    def __str__(self):
        return f"{self.customer_name}: {self.headline}"


class TestimonialAsset(models.Model):
    class AssetType(models.TextChoices):
        IMAGE = "image", "Image"
        LOGO = "logo", "Logo"

    testimonial = models.ForeignKey(
        Testimonial, on_delete=models.CASCADE, related_name="assets"
    )
    asset_type = models.CharField(max_length=20, choices=AssetType.choices)
    file = models.FileField(upload_to="testimonials/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]

    def __str__(self):
        return f"{self.testimonial.customer_name} - {self.asset_type}"











