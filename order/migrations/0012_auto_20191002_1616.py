# Generated by Django 2.2.2 on 2019-10-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20191002_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shop_user',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='ABC', max_length=120, unique=True),
        ),
    ]
