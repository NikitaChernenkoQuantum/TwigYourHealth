# Generated by Django 2.0.6 on 2018-06-07 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deceases', '0003_auto_20180527_1947'),
        ('accounts', '0002_auto_20180526_0926'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='doctorsphere',
            unique_together={('doctor', 'sphere')},
        ),
    ]
