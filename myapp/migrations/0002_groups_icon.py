# Generated by Django 2.0.9 on 2024-07-04 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='icon',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]