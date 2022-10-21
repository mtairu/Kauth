# Generated by Django 4.1.2 on 2022-10-09 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("kauthappusersapi", "0003_credential_realm"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientAccessToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("access_token", models.TextField(unique=True)),
                ("refresh_token", models.TextField(null=True, unique=True)),
                ("issued_at", models.DateTimeField(auto_now=True)),
                ("expires", models.DateTimeField()),
                ("is_expired", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]