# Generated by Django 4.2.4 on 2023-09-12 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0008_urlhitdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlhitdetail',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='functions.url'),
        ),
    ]
