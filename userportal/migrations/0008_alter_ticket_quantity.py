# Generated by Django 5.1.3 on 2024-12-12 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userportal', '0007_ticket_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
