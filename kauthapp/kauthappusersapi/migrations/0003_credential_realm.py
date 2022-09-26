# Generated by Django 4.1.1 on 2022-09-25 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kauthappusersapi", "0002_credential"),
    ]

    operations = [
        migrations.AddField(
            model_name="credential",
            name="realm",
            field=models.CharField(default="KEYCLOAK", max_length=8, unique=True),
        ),
    ]