from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, validator

from oda_wd_client.base.types import File, WorkdayReferenceBaseModel
from oda_wd_client.base.utils import parse_workday_date
from oda_wd_client.service.financial_management.types import (
    Company,
    CostCenterWorktag,
    Currency,
    ProjectWorktag,
    SpendCategory,
)

# All public imports should be done through oda_wd_client.types.resource_management
__all__: list = []


class TaxApplicability(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Tax_ApplicabilityObjectType  # noqa
    """

    _class_name = "Tax_ApplicabilityObject"
    workday_id: str
    workday_id_type: Literal["Tax_Applicability_ID"] = "Tax_Applicability_ID"
    # Code is human-readable text but not critical, so we default to empty string
    code: str = ""
    taxable: bool = True


class TaxOption(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Tax_OptionObjectType  # noqa
    """

    _class_name = "Tax_OptionObject"
    workday_id: str
    workday_id_type: Literal["Tax_Option_ID"] = "Tax_Option_ID"


class TaxCode(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Tax_CodeObjectType  # noqa
    """

    _class_name = "Tax_CodeObject"
    workday_id: str
    workday_id_type: Literal["Tax_Code_ID"] = "Tax_Code_ID"


class SupplierStatus(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Get_Suppliers.html#Supplier_Status_DataType  # noqa
    """

    class WorkdayID(str, Enum):
        active = "ACTIVE"
        inactive = "INACTIVE"

    _class_name = "Business_Entity_Status_ValueObject"
    workday_id: WorkdayID
    workday_id_type: Literal[
        "Business_Entity_Status_Value_ID"
    ] = "Business_Entity_Status_Value_ID"


class Supplier(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Get_Suppliers.html#SupplierType  # noqa
    """

    _class_name = "SupplierObject"
    workday_id: str
    workday_id_type: Literal["Supplier_ID"] = "Supplier_ID"
    status: SupplierStatus | None = None
    reference_id: str | None
    name: str | None
    payment_terms: str | None
    address: str | None
    phone: str | None
    email: str | None
    url: str | None
    currency: str | None
    bank_account: str | None
    iban: str | None
    primary_tax_id: str | None


class TaxRate(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Tax_RateObjectType  # noqa
    """

    _class_name = "Tax_RateObject"
    workday_id: str
    workday_id_type: Literal["Tax_Rate_ID"] = "Tax_Rate_ID"


class TaxRecoverability(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Tax_RecoverabilityObjectType  # noqa
    """

    _class_name = "Tax_RecoverabilityObject"
    workday_id: str
    workday_id_type: Literal[
        "Tax_Recoverability_Object_ID"
    ] = "Tax_Recoverability_Object_ID"


class TaxRateOptionsData(BaseModel):

    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Tax_Rate_Options_DataType  # noqa

    With some (in)sane defaults
    """

    tax_rate: TaxRate
    tax_recoverability: TaxRecoverability = TaxRecoverability(
        workday_id="Fully_Recoverable"
    )
    tax_option: TaxOption = TaxOption(workday_id="CALC_TAX_DUE")


class FinancialAttachmentData(File):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Financials_Attachment_DataType  # noqa
    """

    field_type = "Financials_Attachment_DataType"


class PrepaidAmortizationType(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Prepaid_Amortization_TypeObjectType  # noqa
    """

    class WorkdayID(str, Enum):
        manual = "Manual"
        schedule = "Schedule"

    _class_name = "Prepaid_Amortization_TypeObject"
    workday_id: WorkdayID
    workday_id_type: Literal[
        "Prepayment_Release_Type_ID"
    ] = "Prepayment_Release_Type_ID"


class AdditionalReferenceType(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v41.1/Submit_Supplier_Invoice.html#Additional_Reference_TypeObjectType  # noqa
    """

    _class_name = "Additional_Reference_TypeObject"
    workday_id_type: Literal[
        "Additional_Reference_Type_ID"
    ] = "Additional_Reference_Type_ID"


class InvoiceAdjustmentReason(WorkdayReferenceBaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice_Adjustment.html#Invoice_Adjustment_ReasonObjectType  # noqa
    """

    _class_name = "Invoice_Adjustment_ReasonObject"
    workday_id_type: Literal["Adjustment_Reason_ID"] = "Adjustment_Reason_ID"


class SupplierInvoiceLine(BaseModel):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Supplier_Invoice_Line_Replacement_DataType  # noqa
    """

    order: int | None
    quantity: Decimal = Field(max_digits=22, decimal_places=2, default=Decimal(0))
    description: str = "-No description-"
    tax_rate_options_data: TaxRateOptionsData | None
    tax_applicability: TaxApplicability | None
    tax_code: TaxCode | None
    spend_category: SpendCategory | None
    cost_center: CostCenterWorktag | None
    project: ProjectWorktag | None
    # Incl. VAT
    gross_amount: Decimal = Field(max_digits=18, decimal_places=3)
    # Excl. VAT
    net_amount: Decimal | None = Field(max_digits=18, decimal_places=3)
    tax_amount: Decimal | None = Field(max_digits=18, decimal_places=3)
    budget_date: date | None


class BaseSupplierInvoice(WorkdayReferenceBaseModel):
    """
    Used as base class for SupplierInvoice and SupplierInvoiceAdjustment

    Main reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Supplier_Invoice_DataType  # noqa
    """

    invoice_number: str | None
    company: Company
    currency: Currency
    supplier: Supplier
    due_date: date
    total_amount: Decimal = Field(max_digits=26, decimal_places=6)
    tax_amount: Decimal = Field(max_digits=26, decimal_places=6)
    tax_option: TaxOption | None
    additional_reference_number: str | None
    additional_type_reference: AdditionalReferenceType | None
    external_po_number: str | None
    prepayment_release_type_reference: PrepaidAmortizationType | None = None

    lines: list[SupplierInvoiceLine]
    attachments: list[FinancialAttachmentData] | None

    # Submit to business process rather than uploading invoice in draft mode
    submit: bool = True
    # Should not be edited inside Workday, only through API
    locked_in_workday: bool = True


class SupplierInvoice(BaseSupplierInvoice):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice.html#Supplier_Invoice_DataType  # noqa
    """

    workday_id_type: Literal[
        "Supplier_Invoice_Reference_ID"
    ] = "Supplier_Invoice_Reference_ID"

    invoice_date: date
    prepaid: bool = False

    _normalize_dates = validator("invoice_date", "due_date", allow_reuse=True)(
        parse_workday_date
    )


class SupplierInvoiceAdjustment(BaseSupplierInvoice):
    """
    Reference: https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v40.2/Submit_Supplier_Invoice_Adjustment.html#Supplier_Invoice_Adjustment_DataType  # noqa
    """

    workday_id_type: Literal[
        "Supplier_Invoice_Adjustment_Reference_ID"
    ] = "Supplier_Invoice_Adjustment_Reference_ID"

    adjustment_date: date
    adjustment_reason: InvoiceAdjustmentReason = InvoiceAdjustmentReason(
        workday_id="Other_Terms"
    )

    _normalize_dates = validator("adjustment_date", "due_date", allow_reuse=True)(
        parse_workday_date
    )
