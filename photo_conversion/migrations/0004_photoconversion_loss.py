# Generated by Django 4.2.9 on 2024-03-08 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_conversion', '0003_alter_photoconversion_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoconversion',
            name='loss',
            field=models.FloatField(blank=True, null=True),
        ),
    ]