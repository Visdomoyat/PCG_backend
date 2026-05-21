from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content_app", "0006_galleryitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testimonial",
            name="customer_email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
    ]
