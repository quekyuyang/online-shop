# Generated by Django 4.0.3 on 2022-05-03 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_image_thumbnail'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='ProductImage',
        ),
    ]