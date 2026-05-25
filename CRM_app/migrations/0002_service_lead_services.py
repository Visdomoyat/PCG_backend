from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CRM_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["sort_order", "name"],
            },
        ),
        migrations.AddField(
            model_name="lead",
            name="services",
            field=models.ManyToManyField(blank=True, related_name="leads", to="CRM_app.service"),
        ),
    ]
