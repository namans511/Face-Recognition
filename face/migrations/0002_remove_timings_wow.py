# Generated by Django 3.2.12 on 2022-05-05 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timings',
            name='wow',
        ),
    ]