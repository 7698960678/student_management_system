# Generated by Django 5.0.1 on 2024-02-06 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Image Id'),
        ),
    ]