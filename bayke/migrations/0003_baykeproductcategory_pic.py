# Generated by Django 4.2 on 2023-04-27 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bayke', '0002_baykeproductcategory_is_nav'),
    ]

    operations = [
        migrations.AddField(
            model_name='baykeproductcategory',
            name='pic',
            field=models.ImageField(blank=True, default='default/cate.png', max_length=200, upload_to='product/cate/', verbose_name='推荐图'),
        ),
    ]