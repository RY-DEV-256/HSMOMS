# Generated by Django 5.0.6 on 2024-06-15 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsmoms_app', '0007_prescriptionfeedback_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescriptionfeedback',
            name='patient_id',
        ),
        migrations.AddField(
            model_name='prescriptionfeedback',
            name='prescription_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hsmoms_app.prescription'),
        ),
    ]
