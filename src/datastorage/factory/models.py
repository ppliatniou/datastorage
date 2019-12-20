from django.db import models
from django.contrib.postgres.fields import JSONField


class Factory(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    version = models.IntegerField()
    locked = models.BooleanField(default=True)
    storage = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'version')

