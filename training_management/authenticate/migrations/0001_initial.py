# Generated by Django 2.1.3 on 2019-04-12 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15)),
                ('role', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('topic_interest', models.CharField(max_length=50)),
                ('notes', models.CharField(max_length=300)),
            ],
        ),
    ]
