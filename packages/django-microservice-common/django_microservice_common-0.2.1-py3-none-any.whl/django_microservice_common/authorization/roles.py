from enum import auto

from django.db import models
from django.utils.translation import gettext as _

from ..authorization.enums import StrEnum


class UserRoles(StrEnum, models.TextChoices):
    ADMIN = auto(), _("Administrator")
    USER = auto(), _("User")
