"""Volume handlers for MCP actions."""

from typing import Any

from src.mcp_instance import mcp
from src.models.volumes import CreateVolumeRequest, UpdateVolumeRequest, VolumeType

from .base import BaseHandler

handler = BaseHandler()


@mcp.tool(
    name="create_volume", title="Create Volume", description="Create a new volume"
)
async def create_volume(
    name: str,
    size: int,
    volume_type: str = "ssd",
    description: str | None = None,
    availability_zone: str | None = None,
    encrypted: bool = False,
    source_volume_id: int | None = None,
    snapshot_id: int | None = None,
) -> dict[str, Any]:
    """Create a new volume."""
    request = CreateVolumeRequest(
        name=name,
        size=size,
        volume_type=VolumeType(volume_type),
        description=description,
        availability_zone=availability_zone,
        encrypted=encrypted,
        source_volume_id=source_volume_id,
        snapshot_id=snapshot_id,
    )

    response = await handler.client.create_volume(
        **request.model_dump(exclude_none=True)
    )
    validated = await handler.validate_response(response, "create_volume")

    return handler.format_success_response(
        f"Volume '{name}' created successfully",
        data=validated,
    )


@mcp.tool(name="list_volumes", title="List Volumes", description="List all volumes")
async def list_volumes(
    page: int | None = None,
    page_size: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    """List all volumes."""
    response = await handler.client.list_volumes(
        page=page,
        page_size=page_size,
        search=search,
    )

    validated = await handler.validate_response(response, "list_volumes")

    return handler.format_list_response(
        items=validated.get("results", []),
        total=validated.get("count"),
        page=page,
        page_size=page_size,
    )


@mcp.tool(
    name="get_volume", title="Get Volume Details", description="Get volume details"
)
async def get_volume(volume_id: int) -> dict[str, Any]:
    """Get volume details."""
    response = await handler.client.get_volume(volume_id)
    validated = await handler.validate_response(response, "get_volume")

    return handler.format_success_response(
        f"Retrieved details for volume {volume_id}",
        data=validated,
    )


@mcp.tool(name="update_volume", title="Update Volume", description="Update a volume")
async def update_volume(
    volume_id: int,
    name: str | None = None,
    description: str | None = None,
    size: int | None = None,
) -> dict[str, Any]:
    """Update a volume."""
    request = UpdateVolumeRequest(
        name=name,
        description=description,
        size=size,
    )

    # Only include non-None values
    update_data = request.model_dump(exclude_none=True)

    if not update_data:
        return handler.format_success_response(
            "No updates specified for volume",
            volume_id=volume_id,
        )

    response = await handler.client.update_volume(volume_id, **update_data)
    validated = await handler.validate_response(response, "update_volume")

    return handler.format_success_response(
        f"Volume {volume_id} updated successfully",
        data=validated,
    )


@mcp.tool(name="delete_volume", title="Delete Volume", description="Delete a volume")
async def delete_volume(volume_id: int) -> dict[str, Any]:
    """Delete a volume."""
    response = await handler.client.delete_volume(volume_id)
    await handler.validate_response(response, "delete_volume")

    return handler.format_success_response(
        f"Volume {volume_id} deleted successfully",
        volume_id=volume_id,
        action="delete",
    )


@mcp.tool(
    name="list_volume_types",
    title="List Volume Types",
    description="List available volume types",
)
async def list_volume_types() -> dict[str, Any]:
    """List available volume types."""
    response = await handler.client.list_volume_types()
    validated = await handler.validate_response(response, "list_volume_types")

    volume_types = validated.get("volume_types", [])
    return handler.format_list_response(
        items=volume_types,
        total=len(volume_types),
    )


@mcp.tool(
    name="update_volume_attachment",
    title="Update Volume Attachment",
    description="Update volume attachment",
)
async def update_volume_attachment(
    volume_id: int,
    vm_id: int,
    device: str | None = None,
) -> dict[str, Any]:
    """Update volume attachment."""
    attachment_data = {
        "vm_id": vm_id,
    }
    if device:
        attachment_data["device"] = device

    response = await handler.client.update_volume_attachment(volume_id, attachment_data)
    validated = await handler.validate_response(response, "update_volume_attachment")

    return handler.format_success_response(
        f"Volume {volume_id} attachment updated successfully",
        data=validated,
    )
