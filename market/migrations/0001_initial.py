# Generated by Django 2.0.1 on 2018-01-07 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnedStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_purchase', models.DateTimeField(null=True)),
                ('price_at_purchase', models.FloatField()),
                ('quantity', models.IntegerField(null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('name', models.CharField(help_text='Enter the name of stock', max_length=250, primary_key=True, serialize=False)),
                ('symbol', models.CharField(help_text='Enter the stocks name', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='unique ID for trader', primary_key=True, serialize=False)),
                ('cash', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ownedstock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Stock'),
        ),
    ]