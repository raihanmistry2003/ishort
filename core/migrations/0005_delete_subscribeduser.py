# Generated by Django 4.2.4 on 2023-08-18 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_pricingplan_plan_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubscribedUser',
        ),
    ]
