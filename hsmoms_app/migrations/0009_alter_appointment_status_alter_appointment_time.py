# Generated by Django 5.0.6 on 2024-06-15 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsmoms_app', '0008_remove_prescriptionfeedback_patient_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(max_length=50),
        ),
    ]