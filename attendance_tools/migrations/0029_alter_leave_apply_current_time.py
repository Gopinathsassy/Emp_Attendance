# Generated by Django 4.0.6 on 2022-07-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tools', '0028_alter_leave_apply_current_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave_apply',
            name='current_time',
            field=models.CharField(default='', max_length=50),
        ),
    ]