from django.db import models

from apps.core.querysets import BaseModelQuerySet


class ArchiveMixin:
    """
    Archive Mixin used in the manager
    """
    def archived(self):
        return self.filter(is_archived=True)

    def restored(self):
        return self.filter(is_archived=False)

    def unarchived(self):
        return self.filter(is_archived=False)

    def archive(self):
        self.get_queryset().archive()

    def restore(self):
        self.get_queryset().restore()


class BaseModelManager(models.Manager, ArchiveMixin):
    """
    Base Model Manager used in the project, Used in all models
    """
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db)
