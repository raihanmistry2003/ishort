# Generated by Django 4.2.4 on 2023-09-10 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_userloginhistory_browser_userloginhistory_os_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userloginhistory',
            name='device_name',
        ),
        migrations.AddField(
            model_name='userloginhistory',
            name='city',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='userloginhistory',
            name='country',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
