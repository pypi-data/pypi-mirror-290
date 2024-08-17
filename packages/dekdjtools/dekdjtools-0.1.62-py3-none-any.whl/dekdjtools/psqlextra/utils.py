from django.db import connections


def has_psqlextra_backend():
    return any(database for database in connections.databases.values() if "psqlextra" in database["ENGINE"])


def real_makemigrations():
    return 'pgmakemigrations' if has_psqlextra_backend() else 'makemigrations'
