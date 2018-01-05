# Generated by Django 2.0.1 on 2018-01-04 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='id',
        ),
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(help_text='Enter the stocks name', max_length=20, primary_key=True, serialize=False),
        ),
    ]
