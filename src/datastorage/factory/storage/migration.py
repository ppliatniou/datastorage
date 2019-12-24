from django.db import connection, transaction

from factory.models import Storage
from factory.storage.registry import field_registry
from factory.constants import STORAGE_TABLE_PREFIX

__all__ = (
    'perform_migration',
    'create_migration_diff',
)

SQL_CREATE_TABLE = """
CREATE TABLE {table_name}(
{fields},
version integer NOT NULL,
created_at timestamp with time zone NOT NULL,
updated_at timestamp with time zone NOT NULL
)
"""

SQL_ALTER_TABLE = """
ALTER TABLE {table_name} ADD COLUMN {field_definition};
"""


def create_migration_diff(previous, latest):
    if previous is None:
        return latest.definition
    else:
        previous_field_names = [f["name"] for f in previous.definition["fields"]]
        return {
            "fields": [
                f
                for f in latest.definition["fields"]
                if f["name"] not in previous_field_names
            ]
        }


def perform_migration(migration):
    operate_table_queries = []
    if migration.version == 1:
        key_field = field_registry.get_item(migration.definition["key"]["type"])
        db_table_fields = [
            key_field.sql_def(migration.definition["key"], is_pk=True)
        ]
        for def_field in migration.definition["fields"]:
            field = field_registry.get_item(def_field["type"])
            db_table_fields.append(field.sql_def(def_field))
        operate_table_queries.append(SQL_CREATE_TABLE.format(
            table_name=STORAGE_TABLE_PREFIX.format(migration.name.lower()),
            fields=", ".join(db_table_fields)
        ))
    else:
        for def_field in migration.definition["fields"]:
            field = field_registry.get_item(def_field["type"])
            operate_table_queries.append(SQL_ALTER_TABLE.format(
                table_name=STORAGE_TABLE_PREFIX.format(migration.name.lower()),
                field_definition=field.sql_def(def_field)
            ))
    
    with transaction.atomic():
        cursor = connection.cursor()
        for query in operate_table_queries:
            cursor.execute(query)
        cursor.close()
        migration.applied = True
        migration.save()
        Storage.objects.filter(name=migration.name).update(locked=False)
