# Generated by Django 2.2.2 on 2019-10-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_order_shop_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
