# Generated manually for GalleryItem

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("content_app", "0005_sitecontent_is_published"),
    ]

    operations = [
        migrations.CreateModel(
            name="GalleryItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Label shown in admin and API.", max_length=200)),
                (
                    "media_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")],
                        max_length=10,
                    ),
                ),
                ("file", models.FileField(upload_to="gallery/")),
                ("is_published", models.BooleanField(default=False)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_gallery_items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Gallery item",
                "verbose_name_plural": "Gallery items",
                "ordering": ["sort_order", "-updated_at"],
            },
        ),
    ]
