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
version integer NOT NULL,
created_at timestamp with time zone NOT NULL,
updated_at timestamp with time zone NOT NULL
)
"""

SQL_ALTER_TABLE = """
ALTER TABLE {table_name} {statement};
"""

SQL_UPDATE_TABLE = """
UPDATE {table_name} {statement}
"""

SQL_CREATE_INDEX = """
CREATE INDEX {idx_name} ON {table_name} ({field_name});
"""

SQL_OPERATIONS = {
    "alter": SQL_ALTER_TABLE,
    "update": SQL_UPDATE_TABLE,
    "index": SQL_CREATE_INDEX
}


def get_operation(op):
    return SQL_OPERATIONS[op]


def create_migration_diff(previous, latest):
    if previous is None:
        return latest.definition
    else:
        previous_field_names = previous.get_field_names()
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
        operate_table_queries.append(SQL_CREATE_TABLE.format(
            table_name=STORAGE_TABLE_PREFIX.format(migration.name.lower())
        ))
        
        key_field = field_registry.get(migration.definition["key"]["type"])
        operate_table_queries.append(
            SQL_ALTER_TABLE.format(
                table_name=STORAGE_TABLE_PREFIX.format(migration.name.lower()),
                statement=key_field.sql_def(migration.definition["key"], is_pk=True)[0][1]
            )
        )
        
    for def_field in migration.definition["fields"]:
        field = field_registry.get(def_field["type"])
        operate_table_queries.extend([
            get_operation(op).format(
                table_name=STORAGE_TABLE_PREFIX.format(migration.name.lower()),
                statement=statement
            )
            for op, statement in field.sql_def(def_field)
        ])
        if field.index_def(def_field):
            operate_table_queries.append(
                get_operation("index").format(
                    idx_name='{}_{}_idx'.format(migration.name.lower(), def_field["name"]),
                    table_name=STORAGE_TABLE_PREFIX.format(migration.name.lower()),
                    field_name=def_field["name"]
                )
            )
    
    with connection.cursor() as cursor:
        with transaction.atomic():
            for query in operate_table_queries:
                cursor.execute(query)
            migration.applied = True
            migration.save()
            Storage.objects.filter(name=migration.name).update(locked=False)
