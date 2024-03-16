from django.db import models
import uuid


class Ticket(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=128,
        unique=True
    )

    def __str__(self):
        return self.name
