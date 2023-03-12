import uuid

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=(
    "Phone number must be entered in the format:'+999999999'.Up to 15 digits"
    " allowed."))


class Account(TimeStampedModel):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,
                            primary_key=True)
    phone = models.TextField(validators=[phone_regex])


class AdminAccount(Account):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                related_name="admin_user", null=True)


class UserAccount(Account):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                related_name="users", null=True)
