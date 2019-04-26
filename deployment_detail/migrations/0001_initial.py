# Generated by Django 2.1.3 on 2019-04-14 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeploymentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliverable_id', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('project_code', models.CharField(max_length=50)),
                ('course_order', models.CharField(max_length=200)),
                ('curriculum_name', models.CharField(max_length=200)),
                ('curriculum_description', models.CharField(max_length=200)),
                ('course_name', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=500)),
                ('days_to_complete_course', models.IntegerField()),
                ('course_duration', models.CharField(max_length=20)),
                ('course_key_words', models.CharField(max_length=200)),
                ('course_exam', models.CharField(max_length=10)),
                ('approved_audience', models.CharField(max_length=100)),
            ],
        ),
    ]
