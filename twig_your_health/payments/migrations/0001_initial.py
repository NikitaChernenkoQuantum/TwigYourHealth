# Generated by Django 2.0.2 on 2018-05-26 09:26

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20180526_0926'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('sum', models.PositiveIntegerField(verbose_name='sum to pay')),
                ('payed', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(limit_choices_to=django.db.models.query_utils.Q(django.db.models.query_utils.Q(('app_label', 'communications'), ('model', 'CallEntity'), _connector='AND'), django.db.models.query_utils.Q(('app_label', 'communications'), ('model', 'ChatEntity'), _connector='AND'), django.db.models.query_utils.Q(('app_label', 'timetables'), ('model', 'Visit'), _connector='AND'), _connector='OR'), on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payments.Order')),
                ('patient', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.Patient')),
            ],
        ),
    ]
