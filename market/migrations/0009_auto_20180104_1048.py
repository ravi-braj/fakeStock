# Generated by Django 2.0.1 on 2018-01-04 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_auto_20180104_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trader',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
