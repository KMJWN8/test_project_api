# Generated by Django 5.1.7 on 2025-04-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divisions', '0003_alter_employee_options_remove_department_leader_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='team',
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='team_members', to='divisions.employee'),
        ),
    ]
