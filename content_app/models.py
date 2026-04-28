from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

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
    personal_bio = models.TextField()
    professional_bio = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_site_content",
    )

    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
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
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
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
