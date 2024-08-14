import os
from datetime import date

from _decimal import Decimal

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from model_utils import FieldTracker
from django.urls import reverse

from core_models import constants
from core_models.app.models import User, Currency, Company
from .base import BaseModelAbstract
from .. import NotificationManager
from ...utils import send_invoice_update_to_seller


def doc_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'bill-of-ladings/{instance.id}{ext}'


def po_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'purchase-orders/{instance.id}{ext}'


def po_inv_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'purchase-orders/INV_{instance.id}{ext}'


class Invoice(BaseModelAbstract, models.Model):
    # seller = models.ForeignKey(User, models.SET_NULL, null=True, blank=True,
    #                            related_name='sent_invoices')
    # buyer = models.ForeignKey(User, models.SET_NULL, null=True, blank=True,
    #                           related_name='received_invoices')
    # financier = models.ForeignKey(User, models.SET_NULL, null=True, blank=True,
    #                               related_name='funded_invoices')
    seller_company = models.ForeignKey(Company, models.SET_NULL, null=True,
                                       blank=True,
                                       related_name='sent_invoices')
    buyer_company = models.ForeignKey(Company, models.SET_NULL, null=True,
                                      blank=True,
                                      related_name='received_invoices')
    financier_company = models.ForeignKey(Company, models.SET_NULL, null=True,
                                          blank=True,
                                          related_name='funded_invoices')
    type = models.CharField(max_length=1,
                            default=constants.NORMAL_INVOICE_TYPE,
                            choices=constants.INVOICE_TYPES)
    currency = models.ForeignKey(Currency, models.SET_NULL, null=True,
                                 blank=True)
    reference = models.CharField(max_length=20, null=True, blank=True,
                                 editable=False)
    invoice_number = models.CharField(max_length=50, null=False, blank=False)
    subtotal = models.DecimalField(decimal_places=2, max_digits=30, null=False,
                                   blank=False)
    total = models.DecimalField(decimal_places=2, max_digits=30, null=False,
                                blank=False)
    discount = models.DecimalField(decimal_places=2, max_digits=30, default=0)
    tax = models.DecimalField(decimal_places=2, max_digits=30, default=0)
    po_date = models.DateField(null=True, blank=True)
    invoice_date = models.DateField(null=False, blank=False)
    due_date = models.DateField(null=False, blank=False)
    financed_on = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30,
                              choices=constants.INVOICE_STATUSES,
                              default=constants.NEW_INVOICE_STATUS)
    decline_reason = models.TextField(null=True, blank=True)
    recurring = models.BooleanField(default=False)
    seller_risk_percentage = models.FloatField(
        default=0,
        help_text="Auto-picked from Contract"
    )
    buyer_risk_percentage = models.FloatField(
        default=0,
        help_text="Auto-picked from Contract"
    )
    base_rate = models.FloatField(
        default=0, help_text="Auto-picked from Base Rate"
    )
    interest_rate = models.FloatField(default=0, editable=False)
    interest = models.DecimalField(
        decimal_places=2, max_digits=30, default=0,
        help_text="Calculated: This is the amount that goes to the Financier "
                  "as interest/profit"
    )
    liquify_fee = models.DecimalField(
        decimal_places=2, max_digits=30, default=0,
        help_text="This is the platform fee taken for this invoice. Its "
                  "value is gotten from Config."
    )
    buyer_amount = models.DecimalField(
        decimal_places=2, max_digits=30, default=0,
        help_text="Calculated: This is the amount that will be paid back by "
                  "the Buyer"
    )
    seller_amount = models.DecimalField(
        decimal_places=2, max_digits=30, default=0,
        help_text="Calculated: This is the amount that is sent to SME"
    )
    financier_amount = models.DecimalField(
        decimal_places=2, max_digits=30, default=0,
        help_text="Calculated: This is the amount paid by Financier"
    )
    metadata = models.JSONField(null=True, blank=True)
    loan_agreement = CKEditor5Field(editable=False, null=True, blank=True)
    loan_agreement_signed_on = models.DateTimeField(null=True, blank=True)
    loan_agreement_signed_by = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True,
        related_name='signed_loan_agreements'
    )
    rpa = CKEditor5Field(editable=False, null=True, blank=True)
    rpa_signed_on = models.DateTimeField(null=True, blank=True)
    rpa_signed_by = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True,
        related_name='signed_rpas'
    )
    bill_of_lading = models.FileField(null=True, blank=True,
                                      upload_to=doc_upload_to)
    document = models.FileField(null=True, blank=True,
                                upload_to=po_inv_upload_to)
    po_document = models.FileField(null=True, blank=True,
                                   upload_to=po_upload_to)

    tracker = FieldTracker(fields=['status'])

    def get_absolute_url(self):
        return reverse(
            "invoices:detail",
            kwargs={'pk': self.pk}
        )


    @property
    def status_text(self):
        if self.type == constants.PO_INVOICE_TYPE:
            return constants.PO_STATUS_MAP.get(self.status, '-')
        return constants.INVOICE_STATUS_MAP.get(self.status, '-')

    @property
    def buyer(self):
        if not self.buyer_company:
            return None
        return self.buyer_company.users.filter(company_admin=True).first()

    @property
    def seller(self):
        if not self.seller_company:
            return None
        return self.seller_company.users.filter(company_admin=True).first()

    @property
    def financier(self):
        if not self.financier_company:
            return None
        return self.financier_company.users.filter(company_admin=True).first()

    @property
    def passed_due_date(self):
        return date.today() > self.due_date

    def save(self, keep_deleted=False, **kwargs):
        if not self.reference:
            now = timezone.now()
            self.reference = f"LQIN{now.strftime('%Y%m%d%H%M%S')}"
        if self.base_rate and self.seller_risk_percentage and \
                self.buyer_risk_percentage and self.status in (
                constants.NEW_INVOICE_STATUS,
                constants.VALIDATED_INVOICE_STATUS,
                constants.BUYER_VALIDATED_INVOICE_STATUS):
            self.interest_rate = sum(
                [self.base_rate, self.seller_risk_percentage,
                 self.buyer_risk_percentage])
            self.interest = round(self.total * round(Decimal(
                self.interest_rate) / 100, 2), 2)
            self.buyer_amount = self.total
            self.financier_amount = self.total - self.interest
            self.seller_amount = self.financier_amount - self.liquify_fee
        status_changed = self.tracker.has_changed('status') or not self.id
        super(Invoice, self).save(keep_deleted, **kwargs)
        if status_changed:
            NotificationManager.save_invoice_notification(self)
            isPo = self.type == constants.PO_INVOICE_TYPE
            if not isPo and self.status not in (
                    constants.NEW_INVOICE_STATUS,
                    constants.DRAFT_INVOICE_STATUS,
                    constants.BUYER_VALIDATED_INVOICE_STATUS):
                send_invoice_update_to_seller(self)

    def __unicode__(self):
        return self.reference


class InvoiceItem(BaseModelAbstract, models.Model):
    invoice = models.ForeignKey(Invoice, models.CASCADE, related_name="items")
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=20,
                                help_text='Unit Price')
    total = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.DecimalField(default=1, decimal_places=2, max_digits=10)

    def __unicode__(self):
        return f"{self.invoice} item"

    def calc_total(self):
        return self.price * self.quantity

    def save(self, keep_deleted=False, **kwargs):
        self.total = self.calc_total()
        super(InvoiceItem, self).save(keep_deleted, **kwargs)


class InvoiceTransaction(BaseModelAbstract, models.Model):
    invoice = models.ForeignKey(Invoice, models.CASCADE,
                                related_name='transactions')
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    type = models.CharField(choices=constants.TRANSACTION_TYPES, max_length=1)
    reference = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.reference

    def save(self, keep_deleted=False, **kwargs):
        if not self.reference:
            now = timezone.now()
            self.reference = now.strftime('%Y%m%d%H%M%S')
        super().save(keep_deleted=keep_deleted, **kwargs)
