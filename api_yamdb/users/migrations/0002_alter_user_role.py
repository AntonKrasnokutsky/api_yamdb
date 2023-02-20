# Generated by Django 3.2 on 2023-02-20 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Moderator', 'Moderator'), ('User', 'User')], default='user', max_length=9),
        ),
    ]
