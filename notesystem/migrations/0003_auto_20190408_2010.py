# Generated by Django 2.1.7 on 2019-04-08 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesystem', '0002_auto_20190407_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='deadline_date',
            field=models.CharField(max_length=10),
        ),
    ]