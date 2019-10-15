# Generated by Django 2.2.2 on 2019-09-15 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Kart', '0003_auto_20190914_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('status', models.CharField(choices=[('Started', 'Started'), ('Finished', 'Finished')], default='Started', max_length=120)),
                ('kart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Kart.Kart')),
            ],
        ),
    ]
