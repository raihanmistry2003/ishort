# Generated by Django 4.2.4 on 2023-08-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_subscription_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='bulk_url_short',
            field=models.BooleanField(default=False),
        ),
    ]
