# Generated by Django 3.2 on 2023-02-16 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_review_unique_review'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review',
        ),
    ]