# Generated by Django 4.0.5 on 2024-04-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='otp',
            field=models.CharField(max_length=6),
        ),
    ]
