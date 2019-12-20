from django.db import models
from django.contrib.postgres.fields import JSONField


class StorageManager(models.Manager):
    
    def last_versions(self):
        return \
            Storage.objects.filter(
                id__in=Storage.objects.all() \
                    .order_by('name', '-version').distinct('name').values_list('id')
            )


class Storage(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    version = models.IntegerField()
    locked = models.BooleanField(default=True)
    definition = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = StorageManager()
    
    class Meta:
        unique_together = ('name', 'version')

