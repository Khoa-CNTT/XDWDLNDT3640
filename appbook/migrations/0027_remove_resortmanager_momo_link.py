# Generated by Django 5.2 on 2025-05-05 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appbook', '0026_resortmanager_momo_link_resortmanager_momo_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resortmanager',
            name='momo_link',
        ),
    ]
