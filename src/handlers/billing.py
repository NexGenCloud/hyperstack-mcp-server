"""Billing handlers for MCP actions."""

from typing import Any

from src.handlers.base import BaseHandler
from src.mcp_instance import mcp

handler = BaseHandler()


@mcp.tool(
    name="get_billing_status",
    title="Get Billing Status",
    description="Retrieve the current billing account status including balance and account state",
)
async def get_billing_status() -> dict[str, Any]:
    """Get billing account status."""
    response = await handler.client.get_billing_status()
    validated = await handler.validate_response(response, "get_billing_status")

    status = validated.get("status", "unknown")
    balance = validated.get("balance", 0)

    return handler.format_success_response(
        f"Billing account status: {status} (Balance: ${balance})",
        data=validated,
    )


@mcp.tool(
    name="get_billing_usage",
    title="Get Billing Usage",
    description="Get detailed billing usage for a specific time period with optional date filtering",
)
async def get_billing_usage(
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict[str, Any]:
    """Get billing usage for a specified period."""
    response = await handler.client.get_billing_usage(
        start_date=start_date,
        end_date=end_date,
    )
    validated = await handler.validate_response(response, "get_billing_usage")

    total = validated.get("total_amount", 0)
    period_start = validated.get("period_start", "N/A")
    period_end = validated.get("period_end", "N/A")

    return handler.format_success_response(
        f"Billing usage from {period_start} to {period_end}: ${total}",
        data=validated,
    )


@mcp.tool(
    name="get_previous_day_cost",
    title="Get Previous Day Cost",
    description="Retrieve the cost breakdown for the previous day including resource usage charges",
)
async def get_previous_day_cost() -> dict[str, Any]:
    """Get previous day's cost breakdown."""
    response = await handler.client.get_previous_day_cost()
    validated = await handler.validate_response(response, "get_previous_day_cost")

    total_cost = validated.get("total_cost", 0)
    date = validated.get("date", "yesterday")

    return handler.format_success_response(
        f"Previous day cost ({date}): ${total_cost}",
        data=validated,
    )


@mcp.tool(
    name="get_credit_balance",
    title="Get Credit Balance",
    description="Check available credits, total credits allocated, and credit usage information",
)
async def get_credit_balance() -> dict[str, Any]:
    """Get credit balance and details."""
    response = await handler.client.get_credit_balance()
    validated = await handler.validate_response(response, "get_credit_balance")

    available_credits = validated.get("available_credits", 0)
    total_credits = validated.get("total_credits", 0)
    used_credits = validated.get("used_credits", 0)

    return handler.format_success_response(
        f"Credit balance: ${available_credits} available (${used_credits} used of ${total_credits} total)",
        data=validated,
    )


@mcp.tool(
    name="get_payment_history",
    title="Get Payment History",
    description="Retrieve historical payment transactions with pagination support",
)
async def get_payment_history(
    page: int | None = None,
    page_size: int | None = None,
) -> dict[str, Any]:
    """Get payment history."""
    response = await handler.client.get_payment_history(
        page=page,
        page_size=page_size,
    )

    validated = await handler.validate_response(response, "get_payment_history")

    payments = validated.get("payments", [])

    return handler.format_list_response(
        items=payments,
        total=len(payments),
        page=page,
        page_size=page_size,
    )
