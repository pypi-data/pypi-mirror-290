import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from . import Company
from .base import BaseModelAbstract
from core_models.constants import COMPANY_TYPES
from ... import constants


def identity_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'purchase-orders/INV_{instance.id}{ext}'


def address_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'purchase-orders/INV_{instance.id}{ext}'


class User(AbstractUser, BaseModelAbstract):
    """
        Overrides django's default auth model
    """
    USERNAME_FIELD = "email"
    username = None
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "user_type"]
    
    email = models.EmailField(unique=True, null=False, blank=False)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=15, choices=COMPANY_TYPES)
    is_onboarding_complete = models.BooleanField(default=False)
    onboarding_stage = models.IntegerField(default=1)
    reset_token = models.CharField(max_length=10, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    notification_tokens = models.JSONField(blank=True, null=True)
    change_password = models.BooleanField(default=False)
    seen_walkthrough = models.BooleanField(default=False)
    company_admin = models.BooleanField(default=True)
    company = models.ForeignKey(Company, models.CASCADE, null=True,
                                blank=True, related_name="users")


    def buyers(self):
        return self.company.seller_contracts.filter(
            status__in=(
                constants.ACCEPTED_CONTRACT_STATUS,
                constants.VERIFIED_CONTRACT_STATUS
            )
        )

    def sellers(self):
        return self.company.buyer_contracts.filter(
            status__in=(
                constants.ACCEPTED_CONTRACT_STATUS,
                constants.VERIFIED_CONTRACT_STATUS
            )
        )

    @property
    def user_type_description(self):
        return constants.COMPANY_TYPES_MAP.get(self.user_type, 'None')
