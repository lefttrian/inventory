# Generated by Django 3.2.9 on 2021-11-29 11:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0003_alter_stock_inputdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='InputDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 29, 13, 47, 50, 89958)),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('Item', 'LocationCode', 'Store')},
        ),
    ]
