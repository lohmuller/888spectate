# Generated by Django 4.2.6 on 2023-10-22 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spectate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sport',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
