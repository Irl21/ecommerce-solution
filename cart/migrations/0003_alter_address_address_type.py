# Generated by Django 4.1.7 on 2023-02-22 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Address_type',
            field=models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1, null=True),
        ),
    ]