"""Metadata handlers for MCP actions (flavors, environments, stock)."""

from typing import Any

from src.mcp_instance import mcp

from .base import BaseHandler

handler = BaseHandler()


@mcp.tool(
    name="list_flavors",
    title="List Flavors",
    description="List available flavors (instance types)",
)
async def list_flavors(region: str | None = None) -> dict[str, Any]:
    """List available flavors."""
    response = await handler.client.list_flavors(region=region)
    validated = await handler.validate_response(response, "list_flavors")

    flavors = validated.get("flavors", [])
    return handler.format_list_response(
        items=flavors,
        total=len(flavors),
    )


@mcp.tool(
    name="get_flavor", title="Get Flavor Details", description="Get flavor details"
)
async def get_flavor(flavor_id: int) -> dict[str, Any]:
    """Get flavor details."""
    response = await handler.client.get_flavor(flavor_id)
    validated = await handler.validate_response(response, "get_flavor")

    return handler.format_success_response(
        f"Retrieved details for flavor {flavor_id}",
        data=validated,
    )


@mcp.tool(
    name="list_environments",
    title="List Environments",
    description="List available environments (regions)",
)
async def list_environments() -> dict[str, Any]:
    """List available environments."""
    response = await handler.client.list_environments()
    validated = await handler.validate_response(response, "list_environments")

    environments = validated.get("environments", [])
    return handler.format_list_response(
        items=environments,
        total=len(environments),
    )


@mcp.tool(
    name="get_environment",
    title="Get Environment Details",
    description="Get environment details",
)
async def get_environment(environment_id: int) -> dict[str, Any]:
    """Get environment details."""
    response = await handler.client.get_environment(environment_id)
    validated = await handler.validate_response(response, "get_environment")

    return handler.format_success_response(
        f"Retrieved details for environment {environment_id}",
        data=validated,
    )


@mcp.tool(
    name="check_stock",
    title="Check Stock",
    description="Check stock availability for a flavor",
)
async def check_stock(flavor_name: str) -> dict[str, Any]:
    """Check stock availability for a flavor."""
    response = await handler.client.check_stock(flavor_name)
    validated = await handler.validate_response(response, "check_stock")

    stock_info = validated.get("stock", {})
    availability = stock_info.get("status", "unknown")
    available_count = stock_info.get("available_count", 0)

    message = f"Flavor '{flavor_name}' has {available_count} instances available"
    if availability == "out_of_stock":
        message = f"Flavor '{flavor_name}' is currently out of stock"
    elif availability == "limited":
        message = f"Flavor '{flavor_name}' has limited availability ({available_count} instances)"

    return handler.format_success_response(
        message,
        data=stock_info,
    )
