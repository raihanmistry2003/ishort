# Generated by Django 4.2.4 on 2023-09-06 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_subscription_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='subscription',
        ),
        migrations.AddField(
            model_name='payment',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.plan'),
        ),
    ]