# Generated by Django 5.1.1 on 2024-10-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_headset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headset',
            name='barcodeNo',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='venues',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
