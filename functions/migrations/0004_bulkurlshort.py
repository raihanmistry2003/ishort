# Generated by Django 4.2.4 on 2023-08-21 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('functions', '0003_alter_excelfile_excelsheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkUrlShort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(blank=True, max_length=20, verbose_name='Short Url Auto Generated')),
                ('long_url', models.TextField(verbose_name='Long Url')),
                ('url_hit_count', models.PositiveIntegerField(default=0, verbose_name='Url Hit Count')),
                ('url_created_at', models.DateField(auto_now=True)),
                ('url_updated_at', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
