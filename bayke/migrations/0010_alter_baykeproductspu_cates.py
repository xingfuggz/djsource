# Generated by Django 4.2 on 2023-04-23 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bayke', '0009_baykeproductcategory_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baykeproductspu',
            name='cates',
            field=models.ManyToManyField(to='bayke.baykeproductcategory', verbose_name='商品分类'),
        ),
    ]