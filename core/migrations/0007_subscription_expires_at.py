# Generated by Django 4.2.4 on 2023-08-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_plan_subscription_delete_pricingplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
