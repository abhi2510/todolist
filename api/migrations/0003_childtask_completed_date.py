# Generated by Django 2.1.7 on 2019-04-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190328_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='childtask',
            name='completed_date',
            field=models.DateTimeField(null=True),
        ),
    ]
