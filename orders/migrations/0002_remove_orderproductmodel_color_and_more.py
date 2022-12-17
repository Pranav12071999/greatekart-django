# Generated by Django 4.0.2 on 2022-12-15 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variationmodel'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproductmodel',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproductmodel',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderproductmodel',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproductmodel',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.VariationModel'),
        ),
    ]
