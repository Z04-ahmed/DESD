# Generated by Django 4.2 on 2025-05-08 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management', '0013_event_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='community',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management.community'),
            preserve_default=False,
        ),
    ]
