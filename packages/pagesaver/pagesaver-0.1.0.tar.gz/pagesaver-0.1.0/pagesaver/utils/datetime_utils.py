from datetime import datetime

from django.utils import timezone


def get_now_str():
    return timezone.now().astimezone().strftime("%Y%m%d%H%M%S")
