import binascii
import os
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pagesaver.lib.base.models import BaseModel


def _default_expire_time():
    return timezone.now() + APIToken.TOKEN_EXPIRE


class APIToken(BaseModel):
    TOKEN_LENGTH = 32
    TOKEN_EXPIRE = timedelta(days=30)

    expired = models.DateTimeField(_("token expire time"), default=_default_expire_time)
    token = models.TextField(_("token"), blank=True)

    def generate_key(self):
        return binascii.hexlify(os.urandom(int(self.TOKEN_LENGTH / 2))).decode()

    def verify(self):
        return self.check_exp() and len(self.token) == self.TOKEN_LENGTH

    def check_exp(self):
        return timezone.now() < self.expired

    def refresf_exp(self):
        self.expired = timezone.now() + self.TOKEN_EXPIRE
        self.save(update_fields=["expired"])

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = _("api token")
        verbose_name_plural = verbose_name
        db_table = "api_token"
