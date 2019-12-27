from celery import task

from factory.models import StorageMigration

from factory.storage.migration import perform_migration as tool_perform_migration


@task
def perform_migration(migration_id):
    migration = StorageMigration.objects.get(id=migration_id)
    tool_perform_migration(migration)