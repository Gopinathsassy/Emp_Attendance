# Generated by Django 4.0.6 on 2022-07-25 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tools', '0025_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.CharField(default='', max_length=50),
        ),
    ]