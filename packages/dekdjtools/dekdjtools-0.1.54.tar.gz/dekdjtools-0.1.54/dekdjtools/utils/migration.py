import os
from django.conf import settings
from django.apps import apps
from django.db.migrations.recorder import MigrationRecorder
from dektools.file import normal_path

project_dir = normal_path(settings.BASE_DIR)

project_dir_prefix = project_dir + os.path.sep

env_list = [".venv", "venv", "env"]

project_dir_env_list = [os.path.join(project_dir, env) + os.path.sep for env in env_list]


def list_migration_paths():
    result = {}
    for app_config in apps.get_app_configs():
        app_path = app_config.path
        if app_path.startswith(project_dir_prefix) and all(not app_path.startswith(x) for x in project_dir_env_list):
            migrations_path = os.path.join(app_path, 'migrations')
            if os.path.isdir(migrations_path):
                for item in os.listdir(migrations_path):
                    item_path = os.path.join(migrations_path, item)
                    if os.path.isfile(item_path) and item != '__init__.py' and os.path.splitext(item)[-1] == '.py':
                        result.setdefault(app_config.label, set()).add(item_path)
    return project_dir, result


def list_migration_entries():
    result = {}
    for migration in MigrationRecorder.Migration.objects.all():
        result.setdefault(migration.app, set()).add(migration.name)
    return result
