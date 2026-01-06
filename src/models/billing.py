"""Billing models for Hyperstack MCP Server."""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class BillingStatus(str, Enum):
    """Billing account status enum."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    OVERDUE = "overdue"
    TRIAL = "trial"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Payment method enum."""

    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    WIRE_TRANSFER = "wire_transfer"
    CREDITS = "credits"
    INVOICE = "invoice"


class PaymentStatus(str, Enum):
    """Payment status enum."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class ResourceType(str, Enum):
    """Resource type for billing."""

    VIRTUAL_MACHINE = "virtual_machine"
    VOLUME = "volume"
    FLOATING_IP = "floating_ip"
    CLUSTER = "cluster"
    SNAPSHOT = "snapshot"
    BANDWIDTH = "bandwidth"
    SUPPORT = "support"
    OTHER = "other"


class BillingAccount(BaseModel):
    """Billing account model."""

    account_id: str = Field(..., description="Account ID")
    status: BillingStatus = Field(..., description="Account status")
    balance: Decimal = Field(..., description="Current balance")
    credit_balance: Decimal = Field(..., description="Credit balance")
    currency: str = Field(default="USD", description="Currency")
    payment_method: PaymentMethod = Field(..., description="Default payment method")
    billing_email: str = Field(..., description="Billing email")
    company_name: str | None = Field(None, description="Company name")
    tax_id: str | None = Field(None, description="Tax ID")
    billing_address: dict[str, str] | None = Field(None, description="Billing address")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")


class UsageItem(BaseModel):
    """Individual usage item model."""

    resource_id: str = Field(..., description="Resource ID")
    resource_type: ResourceType = Field(..., description="Resource type")
    resource_name: str = Field(..., description="Resource name")
    quantity: Decimal = Field(..., description="Quantity used")
    unit: str = Field(..., description="Unit of measurement")
    rate: Decimal = Field(..., description="Rate per unit")
    amount: Decimal = Field(..., description="Total amount")
    start_time: datetime = Field(..., description="Usage start time")
    end_time: datetime = Field(..., description="Usage end time")
    region: str | None = Field(None, description="Region")
    tags: list[str] = Field(default_factory=list, description="Resource tags")


class BillingUsage(BaseModel):
    """Billing usage summary model."""

    period_start: date = Field(..., description="Billing period start")
    period_end: date = Field(..., description="Billing period end")
    total_amount: Decimal = Field(..., description="Total amount")
    tax_amount: Decimal = Field(..., description="Tax amount")
    discount_amount: Decimal = Field(
        default=Decimal("0"), description="Discount amount"
    )
    credits_applied: Decimal = Field(
        default=Decimal("0"), description="Credits applied"
    )
    currency: str = Field(default="USD", description="Currency")
    items: list[UsageItem] = Field(default_factory=list, description="Usage items")
    summary_by_type: dict[ResourceType, Decimal] = Field(
        default_factory=dict, description="Summary by resource type"
    )


class PreviousDayCost(BaseModel):
    """Previous day cost summary model."""

    date: date = Field(..., description="Date")
    total_cost: Decimal = Field(..., description="Total cost")
    compute_cost: Decimal = Field(..., description="Compute cost")
    storage_cost: Decimal = Field(..., description="Storage cost")
    network_cost: Decimal = Field(..., description="Network cost")
    other_cost: Decimal = Field(..., description="Other costs")
    currency: str = Field(default="USD", description="Currency")
    breakdown: list[UsageItem] = Field(
        default_factory=list, description="Cost breakdown"
    )


class CreditBalance(BaseModel):
    """Credit balance model."""

    total_credits: Decimal = Field(..., description="Total credits")
    used_credits: Decimal = Field(..., description="Used credits")
    available_credits: Decimal = Field(..., description="Available credits")
    expiring_credits: Decimal = Field(
        default=Decimal("0"), description="Expiring credits"
    )
    expiry_date: date | None = Field(None, description="Credits expiry date")
    currency: str = Field(default="USD", description="Currency")
    credit_transactions: list[dict[str, Any]] = Field(
        default_factory=list, description="Recent credit transactions"
    )


class Payment(BaseModel):
    """Payment record model."""

    payment_id: str = Field(..., description="Payment ID")
    date: datetime = Field(..., description="Payment date")
    amount: Decimal = Field(..., description="Payment amount")
    currency: str = Field(default="USD", description="Currency")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    status: PaymentStatus = Field(..., description="Payment status")
    invoice_id: str | None = Field(None, description="Associated invoice ID")
    description: str | None = Field(None, description="Payment description")
    reference: str | None = Field(None, description="Payment reference")


class PaymentHistory(BaseModel):
    """Payment history model."""

    payments: list[Payment] = Field(default_factory=list, description="Payment records")
    total_paid: Decimal = Field(..., description="Total amount paid")
    last_payment_date: datetime | None = Field(None, description="Last payment date")
    next_payment_due: date | None = Field(None, description="Next payment due date")


class BillingAlert(BaseModel):
    """Billing alert configuration model."""

    alert_id: int = Field(..., description="Alert ID")
    name: str = Field(..., description="Alert name")
    threshold_amount: Decimal = Field(..., description="Threshold amount")
    alert_type: str = Field(..., description="Alert type (budget/usage/credit)")
    enabled: bool = Field(default=True, description="Alert enabled")
    notification_emails: list[str] = Field(
        default_factory=list, description="Notification emails"
    )
    last_triggered: datetime | None = Field(None, description="Last triggered time")
