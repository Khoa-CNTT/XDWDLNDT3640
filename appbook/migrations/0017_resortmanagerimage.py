# Generated by Django 4.2.7 on 2025-04-19 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appbook', '0016_remove_notification_is_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResortManagerImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='manager_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='appbook.resortmanager')),
            ],
        ),
    ]
