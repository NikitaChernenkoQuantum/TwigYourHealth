from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand, CommandError, call_command
from django.db.models import FileField  # , get_app, get_models, get_model
from django.apps import apps as django_apps
from optparse import make_option
import os
import shutil
import subprocess

STAGING_MEDIA_PATH = getattr(settings, 'STAGING_MEDIA_PATH', 'staging')
STAGING_MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, STAGING_MEDIA_PATH)


class Command(BaseCommand):
    requires_model_validation = True
    help = (u'This command saves data from DB to staging fixtures. '
            u'Example: \n./manage.py save_staging auth \n'
            u'./manage.py save_staging auth.User\n')

    def add_arguments(self, parser):
        parser.add_argument('app_labels', nargs='+')

    def handle(self, *args, **options):
        if not settings.FIXTURE_DIRS:
            raise CommandError('Add fixtures folder for project root to FIXTURE_DIRS for saving apps not from project')

        env_prefix = ''  # some legacy
        app_labels = options['app_labels']

        for app_label in app_labels:
            try:
                app_label, model_label = app_label.split('.')
                models = [django_apps.get_model(app_label, model_label)]
            except ValueError:
                try:
                    app = django_apps.get_app_config(app_label)
                except ImproperlyConfigured as e:
                    raise CommandError(e)
                models = app.get_models()

            fixtures_dir = settings.FIXTURE_DIRS[0]
            if not os.path.exists(fixtures_dir):
                os.makedirs(fixtures_dir)

            for model in models:
                print('processing model', model)
                meta = model._meta
                model_name = '%s.%s' % (meta.app_label, meta.object_name)

                if not model.objects.exists():
                    continue
                app_model_name = '%s_%s' % (meta.app_label.lower(),
                                            meta.object_name.lower())
                if issubclass(model, AbstractBaseUser):
                    app_model_name = '0_%s' % app_model_name

                fixtures_path = '%s/%sstaging_%s.json' % (fixtures_dir,
                                                          env_prefix,
                                                          app_model_name)
                self.move_files(model)
                print('saving %s' % model_name)

                call_command('dumpdata', model_name, indent=2, natural_foreign=True, stdout=open(fixtures_path, 'w'))

    def move_files(self, model):
        meta = model._meta
        app_label = meta.app_label
        model_name = meta.object_name.lower()

        for field in meta.fields:
            if isinstance(field, FileField) and field in meta.local_fields:
                for obj in model._default_manager.all():
                    file = getattr(obj, field.name)
                    if not file:
                        continue
                    name = file.path.split('/')[-1]
                    dir_path = os.path.join(STAGING_MEDIA_ROOT, app_label, model_name)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    old_path = file.path
                    new_path = os.path.abspath(os.path.join(dir_path, name))
                    if old_path != new_path:
                        while os.path.exists(new_path):
                            name = '_' + name
                            new_path = os.path.abspath(os.path.join(dir_path, name))

                        value = new_path[len(os.path.normpath(settings.MEDIA_ROOT)):]
                        if value.startswith('/'):
                            value = value[1:]

                        try:
                            shutil.copy(old_path, new_path)
                        except IOError:
                            pass

                        setattr(obj, field.name, value)
                        obj.save()
