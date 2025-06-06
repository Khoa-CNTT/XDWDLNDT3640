# Generated by Django 4.2.7 on 2025-04-19 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appbook', '0007_booking_is_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('num_rooms', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_room', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appbook.resort')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
