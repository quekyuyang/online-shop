# Generated by Django 4.0.3 on 2022-05-01 09:21

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_image_image_product_primary_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=shop.models.get_product_dir),
        ),
    ]