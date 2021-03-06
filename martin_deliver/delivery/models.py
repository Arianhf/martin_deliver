import random
import string

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class DeliveryStatus:
    ON_WAY = "on_way"       # delivery is on the way (collection now can see the delivery).
    ACCEPTED = "accepted"   # delivery accepted by a courier.
    RECEIVED = "received"   # delivery received by courier.
    REJECTED = "rejected"   # delivery has not been accepted by any courier in time.
    CANCELED = "canceled"   # delivery canceled by collection.
    DELIVERED = "delivered" # Package received by receiver.
    PENDING = "pending"     # delivery order just created.

    STATUSES = (
        (DELIVERED, _("Delivered")),
        (ON_WAY, _("On the way")),
        (RECEIVED, _("received")),
        (ACCEPTED, _("Accepted")),
        (REJECTED, _("Rejected")),
        (CANCELED, _("Canceled")),
        (PENDING, _("Pending"))
    )

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
    phone_regex = RegexValidator(
        regex=r"^09\d{9}$",
        message=_("phone number must be entered in the format: '09---------'."),
    )
    phone_number = models.CharField(
        max_length=16,
        validators=[phone_regex],
        verbose_name=_("phone number"),
        blank=False,
        null=False,
        unique=True
    )

class Collection(User):
    name = models.CharField(
        max_length=255,
        verbose_name=_("sender name"),
        blank=False,
        null=False,
    )
    webhook_link = models.CharField(
        max_length=255,
        verbose_name=_("webhook address"),
        blank=False,
        null=False,
    )

class Package(SluggedModel):
    sender = models.ForeignKey(
        "Collection",
        on_delete=models.SET_NULL,
        verbose_name=_("sender"),
        help_text=_("sender"),
        db_index=True,
        null=True,
        blank=False,
    )
    courier = models.ForeignKey(
        "Courier",
        on_delete=models.SET_NULL,
        verbose_name=_("sender"),
        help_text=_("sender"),
        db_index=True,
        null=True,
        blank=True,
    )
    phone_regex = RegexValidator(
        regex=r"^09\d{9}$",
        message=_("phone number must be entered in the format: '09---------'."),
    )
    sender_phone_number = models.CharField(
        max_length=16,
        validators=[phone_regex],
        verbose_name=_("sender phone number"),
        blank=False,
        null=False,
    )
    sender_name = models.CharField(
        max_length=255,
        verbose_name=_("sender name"),
        blank=False,
        null=False,
    )
    receiver_phone_number = models.CharField(
        max_length=16,
        validators=[phone_regex],
        verbose_name=_("receiver phone number"),
        blank=False,
        null=False,
    )
    receiver_name = models.CharField(
        max_length=255,
        verbose_name=_("receiver name"),
        blank=False,
        null=False,
    )
    origin_long = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=False,
        null=False,
        verbose_name=_("origin longtitude")
    )
    origin_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=False,
        null=False,
        verbose_name=_("origin latitude")
    )
    origin_address = models.TextField(
        verbose_name=_("origin address"),
    )
    destination_long = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=False,
        verbose_name=_("destination longtitude")
    )
    destination_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=False,
        verbose_name=_("destination latitude")
    )
    destination_address = models.TextField(
        verbose_name=_("address"),
    )
    status = models.CharField(
        max_length=10,
        choices=DeliveryStatus.STATUSES,
        default=DeliveryStatus.PENDING,
        blank=False,
        verbose_name=_("status"),
    )