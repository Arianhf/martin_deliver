import random
import string

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True

class SluggedModel(BaseModel):
    slug = models.CharField(max_length=31, verbose_name=_("slug"), unique=True, blank=True, null=True)

    slug_characters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    slug_prefix = ""
    slug_length = 8

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slug_prefix + ''.join(
                random.SystemRandom().choice(self.slug_characters) for _ in range(self.slug_length))

        super().save(*args, **kwargs)

    def edit_link(self, admin='admin'):
        if not self.id:
            return '---'
        url = reverse('{}:{}_{}_change'.format(admin, self._meta.app_label, self._meta.model_name), args=[self.id])
        return mark_safe('<a class="btn btn-info btn-edit" href="%s">%s</a>' % (url, _("edit")))

    edit_link.short_description = _("edit")

class Courier(User):
    pass


class Collection(User):
    pass
