"""Virtual Machine handlers for MCP actions."""

from typing import Any

from src.exceptions import HyperstackMCPError
from src.mcp_instance import mcp
from src.models.virtual_machines import (
    AddFirewallRuleRequest,
    AddFirewallRuleResponse,
    AttachPublicIPRequest,
    AttachPublicIPResponse,
    AttachVolumeRequest,
    AttachVolumeResponse,
    CreateVMRequest,
    CreateVMResponse,
    DeleteVMRequest,
    DeleteVMResponse,
    DetachPublicIPRequest,
    DetachPublicIPResponse,
    DetachVolumeRequest,
    DetachVolumeResponse,
    GetVMEventsRequest,
    GetVMEventsResponse,
    GetVMRequest,
    GetVMResponse,
    HardRebootVMRequest,
    HardRebootVMResponse,
    HibernateVMRequest,
    HibernateVMResponse,
    ListVMsRequest,
    ListVMsResponse,
    RemoveFirewallRuleRequest,
    RemoveFirewallRuleResponse,
    RestoreVMRequest,
    RestoreVMResponse,
    StartVMRequest,
    StartVMResponse,
    StopVMRequest,
    StopVMResponse,
)

from .base import BaseHandler

handler = BaseHandler()


@mcp.tool(
    name="create_vm",
    title="Create Virtual Machine",
    description="Create a new virtual machine instance with specified configuration",
)
async def create_vm(request: CreateVMRequest) -> dict[str, Any]:
    """Create a new virtual machine."""
    try:
        response = await handler.client.create_vm(request.model_dump(exclude_none=True))
        validated = await handler.validate_response(response, "create_vm", CreateVMResponse)

        return handler.format_success_response(
            "Virtual machine created successfully",
            data=validated,
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "create_vm_error")


@mcp.tool(
    name="list_vms",
    title="List Virtual Machines",
    description="List all virtual machines in your account with filtering options",
)
async def list_vms(request: ListVMsRequest) -> dict[str, Any]:
    """List all virtual machines."""
    try:
        response = await handler.client.list_vms(
            page=request.page,
            page_size=request.pageSize,
            search=request.search,
            environment=request.environment,
        )

        validated = await handler.validate_response(response, "list_vms", ListVMsResponse)

        return handler.format_list_response(
            items=validated.get("instances", []),
            total=validated.get("count"),
            page=validated.get("page"),
            page_size=validated.get("page_size"),
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "list_vms_error")


@mcp.tool(
    name="get_vm",
    title="Get VM Details",
    description="Retrieve detailed information about a specific virtual machine",
)
async def get_vm(request: GetVMRequest) -> dict[str, Any]:
    """Get virtual machine details."""
    vm_id = request.vm_id

    try:
        response = await handler.client.get_vm(vm_id)
        validated = await handler.validate_response(response, "get_vm", GetVMResponse)

        return handler.format_success_response(
            f"Retrieved details for VM {vm_id}",
            data=validated,
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "get_vm_error")


@mcp.tool(
    name="start_vm",
    title="Start VM",
    description="Start a stopped virtual machine instance",
)
async def start_vm(request: StartVMRequest) -> dict[str, Any]:
    """Start a virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.start_vm(vm_id)
        await handler.validate_response(response, "start_vm", StartVMResponse)

        return handler.format_success_response(
            f"Virtual machine {vm_id} started successfully",
            vm_id=vm_id,
            action="start",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "start_vm_error")


@mcp.tool(
    name="stop_vm",
    title="Stop VM",
    description="Stop a running virtual machine instance",
)
async def stop_vm(request: StopVMRequest) -> dict[str, Any]:
    """Stop a virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.stop_vm(vm_id)
        await handler.validate_response(response, "stop_vm", StopVMResponse)

        return handler.format_success_response(
            f"Virtual machine {vm_id} stopped successfully",
            vm_id=vm_id,
            action="stop",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "stop_vm_error")


@mcp.tool(
    name="delete_vm",
    title="Delete VM",
    description="Permanently delete a virtual machine and its resources",
)
async def delete_vm(request: DeleteVMRequest) -> dict[str, Any]:
    """Delete a virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.delete_vm(vm_id)
        await handler.validate_response(response, "delete_vm", DeleteVMResponse)

        return handler.format_success_response(
            f"Virtual machine {vm_id} deleted successfully",
            vm_id=vm_id,
            action="delete",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "delete_vm_error")


@mcp.tool(
    name="hard_reboot_vm",
    title="Hard Reboot VM",
    description="Hard reboot a virtual machine",
)
async def hard_reboot_vm(request: HardRebootVMRequest) -> dict[str, Any]:
    """Hard reboot a virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.hard_reboot_vm(vm_id)
        await handler.validate_response(response, "hard_reboot_vm", HardRebootVMResponse)

        return handler.format_success_response(
            f"Virtual machine {vm_id} hard rebooted successfully",
            vm_id=vm_id,
            action="hard_reboot",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "hard_reboot_vm_error")


@mcp.tool(
    name="hibernate_vm",
    title="Hibernate VM",
    description="Hibernate a virtual machine",
)
async def hibernate_vm(request: HibernateVMRequest) -> dict[str, Any]:
    """Hibernate a virtual machine."""
    vm_id = request.vm_id
    retain_ip = request.retain_ip

    try:
        response = await handler.client.hibernate_vm(vm_id, retain_ip)
        await handler.validate_response(response, "hibernate_vm", HibernateVMResponse)

        return handler.format_success_response(
            f"Virtual machine {vm_id} hibernated successfully with retain_ip='{retain_ip}'",
            vm_id=vm_id,
            action="hibernate",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "hibernate_vm_error")


@mcp.tool(
    name="restore_vm",
    title="Restore VM",
    description="Restore a hibernated virtual machine",
)
async def restore_vm(request: RestoreVMRequest) -> dict[str, Any]:
    """Restore a hibernated virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.restore_vm(vm_id)
        await handler.validate_response(response, "restore_vm", RestoreVMResponse)

        return handler.format_success_response(
            f"Virtual machine {vm_id} restored successfully",
            vm_id=vm_id,
            action="restore",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "restore_vm_error")


@mcp.tool(
    name="attach_volume_to_vm",
    title="Attach Volume to VM",
    description="Attach a volume to a virtual machine",
)
async def attach_volume_to_vm(request: AttachVolumeRequest) -> dict[str, Any]:
    """Attach a volume to a virtual machine."""
    vm_id = request.vm_id
    volume_ids = request.volume_ids

    try:
        response = await handler.client.attach_volume_to_vm(vm_id, volume_ids)
        await handler.validate_response(response, "attach_volume_to_vm", AttachVolumeResponse)

        return handler.format_success_response(
            f"Volume(s) {volume_ids} attached to VM {vm_id} successfully",
            vm_id=vm_id,
            volume_ids=volume_ids,
            action="attach_volume",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "attach_volume_to_vm_error")


@mcp.tool(
    name="detach_volume_from_vm",
    title="Detach Volume from VM",
    description="Detach a volume from a virtual machine",
)
async def detach_volume_from_vm(request: DetachVolumeRequest) -> dict[str, Any]:
    """Detach a volume from a virtual machine."""
    vm_id = request.vm_id
    volume_ids = request.volume_ids

    try:
        response = await handler.client.detach_volume_from_vm(vm_id, volume_ids)
        await handler.validate_response(response, "detach_volume_from_vm", DetachVolumeResponse)

        return handler.format_success_response(
            f"Volume(s) {volume_ids} detached from VM {vm_id} successfully",
            vm_id=vm_id,
            volume_ids=volume_ids,
            action="detach_volume",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "detach_volume_from_vm_error")


@mcp.tool(
    name="attach_floating_ip_to_vm",
    title="Attach Floating IP to VM",
    description="Attach a floating IP to a virtual machine",
)
async def attach_floating_ip_to_vm(request: AttachPublicIPRequest) -> dict[str, Any]:
    """Attach a floating IP to a virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.attach_floating_ip_to_vm(vm_id)
        await handler.validate_response(response, "attach_floating_ip_to_vm", AttachPublicIPResponse)

        return handler.format_success_response(
            f"Floating IP attached to VM {vm_id} successfully",
            vm_id=vm_id,
            action="attach_floating_ip",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "attach_floating_ip_to_vm_error")


@mcp.tool(
    name="detach_floating_ip_from_vm",
    title="Detach Floating IP from VM",
    description="Detach a floating IP from a virtual machine",
)
async def detach_floating_ip_from_vm(request: DetachPublicIPRequest) -> dict[str, Any]:
    """Detach a floating IP from a virtual machine."""
    vm_id = request.vm_id

    try:
        response = await handler.client.detach_floating_ip_from_vm(vm_id)
        await handler.validate_response(response, "detach_floating_ip_from_vm", DetachPublicIPResponse)

        return handler.format_success_response(
            f"Floating IP detached from VM {vm_id} successfully",
            vm_id=vm_id,
            action="detach_floating_ip",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "detach_floating_ip_from_vm_error")


@mcp.tool(
    name="add_firewall_rule",
    title="Add Firewall Rule",
    description="Add a firewall rule to a virtual machine",
)
async def add_firewall_rule(request: AddFirewallRuleRequest) -> dict[str, Any]:
    """Add a firewall rule to a virtual machine."""
    try:
        response = await handler.client.add_firewall_rule(
            request.model_dump(exclude_none=True)
        )
        validated = await handler.validate_response(response, "add_firewall_rule", AddFirewallRuleResponse)

        return handler.format_success_response(
            f"Firewall rule added to VM {request.vm_id} successfully",
            vm_id=request.vm_id,
            rule=validated,
            action="add_firewall_rule",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "add_firewall_rule_error")


@mcp.tool(
    name="remove_firewall_rule",
    title="Remove Firewall Rule",
    description="Remove a firewall rule from a virtual machine",
)
async def remove_firewall_rule(request: RemoveFirewallRuleRequest) -> dict[str, Any]:
    """Remove a firewall rule from a virtual machine."""
    vm_id = request.vm_id
    rule_id = request.rule_id

    try:
        response = await handler.client.remove_firewall_rule(vm_id, rule_id)
        await handler.validate_response(response, "remove_firewall_rule", RemoveFirewallRuleResponse)

        return handler.format_success_response(
            f"Firewall rule {rule_id} removed from VM {vm_id} successfully",
            vm_id=vm_id,
            rule_id=rule_id,
            action="remove_firewall_rule",
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "remove_firewall_rule_error")


@mcp.tool(
    name="get_vm_events",
    title="Get VM Events",
    description="Get virtual machine events",
)
async def get_vm_events(request: GetVMEventsRequest) -> dict[str, Any]:
    """Get virtual machine events."""
    vm_id = request.vm_id

    try:
        response = await handler.client.get_vm_events(vm_id)
        validated = await handler.validate_response(response, "get_vm_events", GetVMEventsResponse)

        events = validated.get("instance_events", [])
        return handler.format_list_response(
            items=events,
            total=len(events),
        )
    except HyperstackMCPError as e:
        return handler.format_error_response(e, "get_vm_events_error")
