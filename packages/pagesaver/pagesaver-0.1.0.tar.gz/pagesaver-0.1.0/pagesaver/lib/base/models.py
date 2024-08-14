import uuid

from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class BaseModelWithUUID(BaseModel):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)

    class Meta:
        abstract = True
