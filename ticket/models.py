from django.db import models
import uuid
from django.conf import settings
from django_celery_beat.models import PeriodicTask


class BaseModel(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_challenges',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class TicketSearch(BaseModel):
    name = models.CharField(
        max_length=128
    )
    url = models.CharField(
        max_length=128
    )
    price_threshold = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    min_availability = models.IntegerField()
    periodic_task = models.ForeignKey(
        PeriodicTask,
        related_name='ticket_searched',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
