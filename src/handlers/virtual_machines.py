"""Virtual Machine handlers for MCP actions."""

from typing import Any

from src.mcp_instance import mcp
from src.models.virtual_machines import (
    CreateVMRequest,
    FirewallDirection,
    FirewallProtocol,
    FirewallRule,
)

from .base import BaseHandler

handler = BaseHandler()


@mcp.tool(
    name="create_vm",
    title="Create Virtual Machine",
    description="Create a new virtual machine instance with specified configuration",
)
async def create_vm(
    name: str,
    environment_id: int,
    flavor_id: int,
    image_id: int | None = None,
    key_name: str | None = None,
    count: int = 1,
    assign_floating_ip: bool = False,
    user_data: str | None = None,
    volume_size: int | None = None,
) -> dict[str, Any]:
    """Create a new virtual machine."""
    request = CreateVMRequest(
        name=name,
        environment_id=environment_id,
        flavor_id=flavor_id,
        image_id=image_id,
        key_name=key_name,
        count=count,
        assign_floating_ip=assign_floating_ip,
        user_data=user_data,
        volume_size=volume_size,
    )

    response = await handler.client.create_vm(**request.model_dump(exclude_none=True))
    validated = await handler.validate_response(response, "create_vm")

    return handler.format_success_response(
        f"Virtual machine '{name}' created successfully",
        data=validated,
    )


@mcp.tool(
    name="list_vms",
    title="List Virtual Machines",
    description="List all virtual machines in your account with filtering options",
)
async def list_vms(
    page: int | None = None,
    page_size: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    """List all virtual machines."""
    response = await handler.client.list_vms(
        page=page,
        page_size=page_size,
        search=search,
    )

    validated = await handler.validate_response(response, "list_vms")

    return handler.format_list_response(
        items=validated.get("results", []),
        total=validated.get("count"),
        page=page,
        page_size=page_size,
    )


@mcp.tool(
    name="get_vm",
    title="Get VM Details",
    description="Retrieve detailed information about a specific virtual machine",
)
async def get_vm(vm_id: int) -> dict[str, Any]:
    """Get virtual machine details."""
    response = await handler.client.get_vm(vm_id)
    validated = await handler.validate_response(response, "get_vm")

    return handler.format_success_response(
        f"Retrieved details for VM {vm_id}",
        data=validated,
    )


@mcp.tool(
    name="start_vm",
    title="Start VM",
    description="Start a stopped virtual machine instance",
)
async def start_vm(vm_id: int) -> dict[str, Any]:
    """Start a virtual machine."""
    response = await handler.client.start_vm(vm_id)
    await handler.validate_response(response, "start_vm")

    return handler.format_success_response(
        f"Virtual machine {vm_id} started successfully",
        vm_id=vm_id,
        action="start",
    )


@mcp.tool(
    name="stop_vm",
    title="Stop VM",
    description="Stop a running virtual machine instance",
)
async def stop_vm(vm_id: int) -> dict[str, Any]:
    """Stop a virtual machine."""
    response = await handler.client.stop_vm(vm_id)
    await handler.validate_response(response, "stop_vm")

    return handler.format_success_response(
        f"Virtual machine {vm_id} stopped successfully",
        vm_id=vm_id,
        action="stop",
    )


@mcp.tool(
    name="delete_vm",
    title="Delete VM",
    description="Permanently delete a virtual machine and its resources",
)
async def delete_vm(vm_id: int) -> dict[str, Any]:
    """Delete a virtual machine."""
    response = await handler.client.delete_vm(vm_id)
    await handler.validate_response(response, "delete_vm")

    return handler.format_success_response(
        f"Virtual machine {vm_id} deleted successfully",
        vm_id=vm_id,
        action="delete",
    )


@mcp.tool(
    name="hard_reboot_vm",
    title="Hard Reboot VM",
    description="Hard reboot a virtual machine",
)
async def hard_reboot_vm(vm_id: int) -> dict[str, Any]:
    """Hard reboot a virtual machine."""
    response = await handler.client.hard_reboot_vm(vm_id)
    await handler.validate_response(response, "hard_reboot_vm")

    return handler.format_success_response(
        f"Virtual machine {vm_id} hard rebooted successfully",
        vm_id=vm_id,
        action="hard_reboot",
    )


@mcp.tool(
    name="hibernate_vm", title="Hibernate VM", description="Hibernate a virtual machine"
)
async def hibernate_vm(vm_id: int) -> dict[str, Any]:
    """Hibernate a virtual machine."""
    response = await handler.client.hibernate_vm(vm_id)
    await handler.validate_response(response, "hibernate_vm")

    return handler.format_success_response(
        f"Virtual machine {vm_id} hibernated successfully",
        vm_id=vm_id,
        action="hibernate",
    )


@mcp.tool(
    name="restore_vm",
    title="Restore VM",
    description="Restore a hibernated virtual machine",
)
async def restore_vm(vm_id: int) -> dict[str, Any]:
    """Restore a hibernated virtual machine."""
    response = await handler.client.restore_vm(vm_id)
    await handler.validate_response(response, "restore_vm")

    return handler.format_success_response(
        f"Virtual machine {vm_id} restored successfully",
        vm_id=vm_id,
        action="restore",
    )


@mcp.tool(
    name="attach_volume_to_vm",
    title="Attach Volume to VM",
    description="Attach a volume to a virtual machine",
)
async def attach_volume_to_vm(vm_id: int, volume_id: int) -> dict[str, Any]:
    """Attach a volume to a virtual machine."""
    response = await handler.client.attach_volume_to_vm(vm_id, volume_id)
    await handler.validate_response(response, "attach_volume_to_vm")

    return handler.format_success_response(
        f"Volume {volume_id} attached to VM {vm_id} successfully",
        vm_id=vm_id,
        volume_id=volume_id,
        action="attach_volume",
    )


@mcp.tool(
    name="detach_volume_from_vm",
    title="Detach Volume from VM",
    description="Detach a volume from a virtual machine",
)
async def detach_volume_from_vm(vm_id: int, volume_id: int) -> dict[str, Any]:
    """Detach a volume from a virtual machine."""
    response = await handler.client.detach_volume_from_vm(vm_id, volume_id)
    await handler.validate_response(response, "detach_volume_from_vm")

    return handler.format_success_response(
        f"Volume {volume_id} detached from VM {vm_id} successfully",
        vm_id=vm_id,
        volume_id=volume_id,
        action="detach_volume",
    )


@mcp.tool(
    name="attach_floating_ip_to_vm",
    title="Attach Floating IP to VM",
    description="Attach a floating IP to a virtual machine",
)
async def attach_floating_ip_to_vm(vm_id: int, floating_ip_id: int) -> dict[str, Any]:
    """Attach a floating IP to a virtual machine."""
    response = await handler.client.attach_floating_ip_to_vm(vm_id, floating_ip_id)
    await handler.validate_response(response, "attach_floating_ip_to_vm")

    return handler.format_success_response(
        f"Floating IP {floating_ip_id} attached to VM {vm_id} successfully",
        vm_id=vm_id,
        floating_ip_id=floating_ip_id,
        action="attach_floating_ip",
    )


@mcp.tool(
    name="detach_floating_ip_from_vm",
    title="Detach Floating IP from VM",
    description="Detach a floating IP from a virtual machine",
)
async def detach_floating_ip_from_vm(vm_id: int, floating_ip_id: int) -> dict[str, Any]:
    """Detach a floating IP from a virtual machine."""
    response = await handler.client.detach_floating_ip_from_vm(vm_id, floating_ip_id)
    await handler.validate_response(response, "detach_floating_ip_from_vm")

    return handler.format_success_response(
        f"Floating IP {floating_ip_id} detached from VM {vm_id} successfully",
        vm_id=vm_id,
        floating_ip_id=floating_ip_id,
        action="detach_floating_ip",
    )


@mcp.tool(
    name="add_firewall_rule",
    title="Add Firewall Rule",
    description="Add a firewall rule to a virtual machine",
)
async def add_firewall_rule(
    vm_id: int,
    protocol: str,
    direction: str,
    port_range_min: int | None = None,
    port_range_max: int | None = None,
    remote_ip_prefix: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Add a firewall rule to a virtual machine."""
    rule = FirewallRule(
        protocol=FirewallProtocol(protocol),
        direction=FirewallDirection(direction),
        port_range_min=port_range_min,
        port_range_max=port_range_max,
        remote_ip_prefix=remote_ip_prefix,
        description=description,
    )

    response = await handler.client.add_firewall_rule(
        vm_id, rule.model_dump(exclude_none=True)
    )
    validated = await handler.validate_response(response, "add_firewall_rule")

    return handler.format_success_response(
        f"Firewall rule added to VM {vm_id} successfully",
        vm_id=vm_id,
        rule=validated,
        action="add_firewall_rule",
    )


@mcp.tool(
    name="remove_firewall_rule",
    title="Remove Firewall Rule",
    description="Remove a firewall rule from a virtual machine",
)
async def remove_firewall_rule(vm_id: int, rule_id: int) -> dict[str, Any]:
    """Remove a firewall rule from a virtual machine."""
    response = await handler.client.remove_firewall_rule(vm_id, rule_id)
    await handler.validate_response(response, "remove_firewall_rule")

    return handler.format_success_response(
        f"Firewall rule {rule_id} removed from VM {vm_id} successfully",
        vm_id=vm_id,
        rule_id=rule_id,
        action="remove_firewall_rule",
    )


@mcp.tool(
    name="get_vm_events",
    title="Get VM Events",
    description="Get virtual machine events",
)
async def get_vm_events(vm_id: int) -> dict[str, Any]:
    """Get virtual machine events."""
    response = await handler.client.get_vm_events(vm_id)
    validated = await handler.validate_response(response, "get_vm_events")

    events = validated.get("events", [])
    return handler.format_list_response(
        items=events,
        total=len(events),
    )
