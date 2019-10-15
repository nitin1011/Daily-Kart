# Generated by Django 2.2.2 on 2019-09-14 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190908_1509'),
        ('Kart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quentity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Products')),
            ],
        ),
        migrations.AddField(
            model_name='kart',
            name='item',
            field=models.ManyToManyField(blank=True, null=True, to='Kart.CartItem'),
        ),
    ]
