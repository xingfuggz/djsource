# Generated by Django 4.2 on 2023-04-22 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bayke', '0005_baykeuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baykeuser',
            name='email',
        ),
    ]
