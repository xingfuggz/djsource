# Generated by Django 4.2 on 2023-04-27 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bayke', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baykeproductcategory',
            name='is_nav',
            field=models.BooleanField(default=True, verbose_name='菜单推荐'),
        ),
    ]
