# Generated by Django 5.2.1 on 2025-05-22 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_sale_customer_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.CharField(default='Flores S.A.', max_length=100),
            preserve_default=False,
        ),
    ]
