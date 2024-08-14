import os

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from .currency import Currency
from .sector import Sector
from .country import Country, Region, City
from .base import BaseModelAbstract
from ... import constants
from ...constants import COMPANY_TYPES


def team_chart_upload_to(_):
    pass


def receivables_and_payables_upload_to(_):
    pass


def logo_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'company-logos/{instance.id}{ext}'


class Company(BaseModelAbstract, models.Model):
    created_by = None
    company_type = models.CharField(max_length=1, choices=COMPANY_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=logo_upload_to, null=True, blank=True)
    sector = models.ForeignKey(Sector, models.SET_NULL, null=True, blank=True)
    registration_number = models.CharField(
        max_length=100, null=True, blank=True
    )
    annual_turnover = models.DecimalField(
        decimal_places=2, max_digits=30, null=True, blank=True
    )
    address_line1 = models.TextField(null=True, blank=True)
    address_line2 = models.TextField(null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(
        Country, models.SET_NULL, blank=True, null=True
    )
    region = models.ForeignKey(
        Region, models.SET_NULL, blank=True, null=True,
        verbose_name="Region/State"
    )
    city = models.ForeignKey(City, models.SET_NULL, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    can_upload_po = models.BooleanField(default=False)
    can_upload_invoice = models.BooleanField(default=True)
    date_verified = models.DateTimeField(null=True, blank=True)
    kyc_status = models.CharField(max_length=30, default="pending")
    kyc_status_reason = models.CharField(max_length=255, null=True, blank=True)

    # @property
    # def kyc_status(self):
    #     if self.is_verified:
    #         return "verified"
    #     if not hasattr(self, 'incorporation_information'):
    #         return "pending"
    #     elif not hasattr(self, 'commercial_information'):
    #         return "pending"
    #     else:
    #         incorporation_information_completed = self.incorporation_information.is_fully_filled(
    #             exempt=['deleted', 'deleted_by_id', 'deleted_at',
    #                     'created_at', 'updated_at', 'is_test',
    #                     'company', 'created_by', 'address']
    #         )
    #         commercial_information_completed = self.commercial_information.is_fully_filled(
    #             exempt=['deleted', 'deleted_by_id', 'deleted_at',
    #                     'created_at', 'updated_at', 'is_test',
    #                     'company', 'created_by']
    #         )
    #         if not (commercial_information_completed or incorporation_information_completed):
    #             return "pending"
    #         else:
    #             return "uploaded"

    @property
    def address(self):
        return f"{self.address_line1}, {self.city}, {self.region}, {self.country}"

    @property
    def user(self):
        return self.users.filter(company_admin=True).first()

    @property
    def invoices(self):
        return self.sent_invoices.filter(type=constants.NORMAL_INVOICE_TYPE)

    @property
    def purchase_orders(self):
        return self.sent_invoices.filter(type=constants.PO_INVOICE_TYPE)

    class Meta:
        verbose_name_plural = 'Companies'

    def save(self, keep_deleted=False, **kwargs):
        self.date_verified = timezone.now() if self.is_verified else None
        super(Company, self).save(keep_deleted, **kwargs)

    def __unicode__(self):
        return f"{self.name}|{self.registration_number}|{self.is_verified}"


def doc_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'company-docs/{instance.id}{ext}'


class CompanyDocument(BaseModelAbstract, models.Model):
    company = models.ForeignKey(Company, models.CASCADE, null=True,
                                blank=True, related_name='docs')
    file = models.FileField(null=False, blank=False, upload_to=doc_upload_to)
    name = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=30, default="Uploaded")
    rejection_note = models.TextField(blank=True)

    class Meta:
        verbose_name = "Company Document"
        verbose_name_plural = "Company Documents"

    def __unicode__(self):
        if not self.company:
            return self.name
        return f"{self.company.name} - {self.name}"


class CompanyIncorporation(BaseModelAbstract, models.Model):
    company = models.OneToOneField(
        Company, models.CASCADE, null=True, blank=True,
        related_name='incorporation_information'
    )
    website = models.URLField(null=False, blank=False)
    external_auditors = ArrayField(
        models.CharField(max_length=255),
        null=False, blank=False
    )
    directors = ArrayField(
        models.CharField(max_length=255),
        null=False, blank=False
    )
    document = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="incorporation_information"
    )
    parent_company = models.CharField(
        max_length=255,
        help_text='Full Legal Corporate Name of Parent Company'
    )
    trading_entity = models.CharField(
        max_length=255,
        help_text='Full legal Corporate Name of Trading Entity (if different)'
    )
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    identity = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="identity"
    )
    proof_of_address = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="proof_of_address"
    )
    proof_of_business_addr = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="proof_of_business_addr"
    )
    share_holding_structure = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="share_holding_structure"
    )
    sample_invoice = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="sample_invoice"
    )

    def __unicode__(self):
        if self.company is None:
            return 'Company Incorporation'
        return f"{self.company.name}"


class CommercialInformation(BaseModelAbstract, models.Model):
    company = models.OneToOneField(
        Company, models.CASCADE, related_name='commercial_information'
    )
    annual_export_vs_domestic = models.FloatField(
        help_text="What percentage of the business’s annual sales/turnover "
                  "is from exports versus domestic sales?",
    )
    monthly_exports = models.DecimalField(
        decimal_places=2,
        max_digits=30,
        help_text="What is the value of your exports monthly?",
    )
    major_currency = models.ForeignKey(
        Currency, models.DO_NOTHING,
        null=False, blank=False,
        help_text="In what currency is the majority of your sales denominated in?"
    )
    financing_payment_terms = ArrayField(
        models.CharField(max_length=100),
        help_text="What are the main types of financing your company uses "
                  "(e.g unsecured loans..etc) and what are the payment terms?",
        null=True, blank=True
    )
    finance_providers = ArrayField(
        models.CharField(max_length=100),
        help_text="Who are your current predominant finance providers?",
        null=True, blank=True
    )
    avg_interest_rate = models.FloatField(
        default=0,
        help_text="What is the current avg. interest rate that your company "
                  "pays for short-term debt (how much are you currently "
                  "paying in interest)?",
    )
    monthly_finance_needed = models.DecimalField(
        default=0,
        decimal_places=2, max_digits=30,
        help_text="How much financing do you need on a monthly basis?",
    )
    accounting_software = ArrayField(
        models.CharField(max_length=100),
        null=False, blank=False,
        help_text="Does your company use any accounting software? "
                  "If so, what is the name of the software and provider?",
    )
    document = models.ForeignKey(
        CompanyDocument, models.DO_NOTHING,
        null=True, blank=True,
        related_name="commercial_information"
    )
    # receivables_and_payables = models.ForeignKey(
    #     CompanyDocument, models.DO_NOTHING,
    #     null=False, blank=False,
    #     help_text="Monthly Receivables & Payables Aging book for last 12 months",
    #     related_name="receivables_and_payables"
    # )
    # sales_ledger = models.ForeignKey(
    #     CompanyDocument, models.DO_NOTHING,
    #     null=False, blank=False,
    #     help_text="Current Open Sales Ledger",
    #     related_name="sales_ledger"
    # )
    # credit_notes = models.ForeignKey(
    #     CompanyDocument, models.DO_NOTHING,
    #     null=False, blank=False,
    #     help_text="Credit Notes/Discounts/Rebates Register",
    #     related_name="credit_notes"
    # )

    def __unicode__(self):
        return f"{self.company}'s Commercial Information"

