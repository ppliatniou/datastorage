from django.db.models import signals

from factory.models import Storage

from storage.model_registry import registry


def remove_storage_from_registry(sender, instance, *args, **kwargs):
    registry.remove(instance.name)


signals.post_save.connect(remove_storage_from_registry, sender=Storage)