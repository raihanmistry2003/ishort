# Generated by Django 4.2.4 on 2023-08-25 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_plan_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.IntegerField(default=365, verbose_name='Plan Duration in Day'),
        ),
    ]
