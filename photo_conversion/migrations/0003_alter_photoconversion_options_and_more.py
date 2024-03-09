# Generated by Django 4.2.9 on 2024-03-08 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_conversion', '0002_rename_projectconversion_photoconversion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photoconversion',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='photoconversion',
            name='accuracy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photoconversion',
            name='reference_id',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]