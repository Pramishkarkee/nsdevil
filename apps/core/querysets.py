from django.db import models
from django.utils import timezone


class ArchiveMixin:
    """
    Mixin for archive instance of model
    """

    def archive(self):
        kwargs = {
            'is_archived': True,
            'updated': timezone.now()
        }
        self.update(**kwargs)

    def restore(self):
        kwargs = {
            'is_archived': False,
            'updated': timezone.now()
        }
        self.update(**kwargs)

    def unarchived(self):
        return self.filter(is_archived=False)


class BaseModelQuerySet(models.QuerySet, ArchiveMixin):
    """
    Base Queryset used in this project
    """
    pass
