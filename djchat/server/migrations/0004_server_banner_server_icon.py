# Generated by Django 5.0.6 on 2024-05-27 10:12

import server.models
import server.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0003_category_icon_alter_channel_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="server",
            name="banner",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=server.models.server_banner_upload_path,
                validators=[server.validators.validate_image_file_extensions],
            ),
        ),
        migrations.AddField(
            model_name="server",
            name="icon",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=server.models.server_icon_upload_path,
                validators=[
                    server.validators.validate_icon_image_size,
                    server.validators.validate_image_file_extensions,
                ],
            ),
        ),
    ]
