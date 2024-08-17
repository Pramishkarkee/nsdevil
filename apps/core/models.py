import uuid

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.managers import BaseModelManager


class BaseModel(models.Model):
    """
    Base Model that will used in this project
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def archive(self):
        if self.is_archived:
            raise DjangoValidationError({
                'non_field_errors': _('Failed - it is already archived.')
            })
        self.is_archived = True
        self.updated_at = timezone.now()
        self.save(update_fields=['is_archived', 'updated'])

    def restore(self):
        if not self.is_archived:
            raise DjangoValidationError({
                'non_field_errors': _('Failed - it is already restored.')
            })
        self.is_archived = False
        self.updated_at = timezone.now()
        self.save(update_fields=['is_archived', 'updated'])