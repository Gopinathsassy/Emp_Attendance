# Generated by Django 4.0.6 on 2022-07-16 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tools', '0008_clockin'),
    ]

    operations = [
        migrations.AddField(
            model_name='clockin',
            name='emp_id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='clockin',
            name='username',
            field=models.CharField(default='', max_length=50),
        ),
    ]