# Generated by Django 3.1 on 2022-04-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listID', models.CharField(max_length=30)),
                ('members', models.JSONField(null=True)),
            ],
        ),
    ]
