# Generated by Django 2.2 on 2022-03-16 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.TextField(max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='major',
            field=models.TextField(max_length=50),
        ),
    ]
