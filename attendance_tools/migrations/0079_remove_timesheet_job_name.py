# Generated by Django 4.0.6 on 2022-09-08 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tools', '0078_rename_billable_status_leave_apply_lead_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='job_name',
        ),
    ]