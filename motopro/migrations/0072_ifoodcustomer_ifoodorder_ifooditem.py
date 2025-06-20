# Generated by Django 5.1 on 2025-05-28 01:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0071_remove_ifoodwebhookevent_delivery_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IfoodCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IfoodOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('ORDER_CREATED', 'Order Created'), ('ORDER_STATUS_CHANGED', 'Status Changed'), ('ORDER_CANCELED', 'Order Canceled')], max_length=50)),
                ('order_id', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('RECEIVED', 'Received'), ('PREPARING', 'Preparing'), ('READY', 'Ready'), ('DELIVERED', 'Delivered'), ('CANCELED', 'Canceled')], max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='motopro.ifoodcustomer')),
            ],
        ),
        migrations.CreateModel(
            name='IfoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='motopro.ifoodorder')),
            ],
        ),
    ]
