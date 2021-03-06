# Generated by Django 2.1.3 on 2019-04-15 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliverable_detail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverable',
            name='content_complete_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='post_processing_complete_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='processing_complete_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='record_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='target_deploy_date',
            field=models.DateTimeField(null=True),
        ),
    ]
