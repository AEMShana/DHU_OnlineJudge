# Generated by Django 3.1 on 2022-04-06 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listName', models.CharField(max_length=30)),
                ('members', models.JSONField(null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
        ),
    ]
