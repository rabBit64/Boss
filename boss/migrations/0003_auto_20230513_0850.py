# Generated by Django 3.2.18 on 2023-05-12 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boss', '0002_address_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[(1, '가공식품'), (2, '농수축산물'), (3, '배달용품'), (4, '주방용품')], max_length=100, verbose_name='카테고리'),
        ),
    ]