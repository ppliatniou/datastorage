from django.db import models
from django.contrib.postgres.fields import JSONField


class FieldHelperMixin:
    def get_key_field_name(self):
        return self.definition.get("key", {}).get("name")
    
    def get_field_names(self):
        return [f["name"] for f in self.definition["fields"]]
    
    def get_index_names(self):
        index_names = []
        if self.get_key_field_name():
            index_names.append(self.get_key_field_name())
        return index_names + [
            f["name"]
            for f in self.definition["fields"]
            if f.get("db_index", False)
        ]


class StorageManager(models.Manager):
    
    def last_versions(self):
        return \
            Storage.objects.filter(
                id__in=Storage.objects.all() \
                    .order_by('name', '-version').distinct('name').values_list('id')
            )


class Storage(FieldHelperMixin, models.Model):
    name = models.CharField(max_length=128, db_index=True)
    version = models.IntegerField()
    locked = models.BooleanField(default=True)
    definition = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = StorageManager()
    
    class Meta:
        unique_together = ('name', 'version')


class StorageMigration(FieldHelperMixin, models.Model):
    name = models.CharField(max_length=128, db_index=True)
    version = models.IntegerField()
    definition = JSONField()
    applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'version')
