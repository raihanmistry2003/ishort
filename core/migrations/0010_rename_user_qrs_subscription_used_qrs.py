# Generated by Django 4.2.4 on 2023-08-23 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_subscription_user_qrs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='user_qrs',
            new_name='used_qrs',
        ),
    ]
