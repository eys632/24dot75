# Generated by Django 5.1.6 on 2025-02-13 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0008_uploadedfile"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadedfile",
            name="is_processed",
            field=models.BooleanField(default=False),
        ),
    ]
