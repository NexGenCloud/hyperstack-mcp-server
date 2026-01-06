"""Virtual Machine models for Hyperstack MCP Server."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from .base import BaseResource


class VMStatus(str, Enum):
    """Virtual machine status enum."""

    ACTIVE = "ACTIVE"
    BUILD = "BUILD"
    DELETED = "DELETED"
    ERROR = "ERROR"
    HARD_REBOOT = "HARD_REBOOT"
    MIGRATING = "MIGRATING"
    PASSWORD = "PASSWORD"  # noqa: S105 - This is a VM status, not a password
    PAUSED = "PAUSED"
    REBOOT = "REBOOT"
    REBUILD = "REBUILD"
    RESCUE = "RESCUE"
    RESIZE = "RESIZE"
    REVERT_RESIZE = "REVERT_RESIZE"
    SHELVED = "SHELVED"
    SHELVED_OFFLOADED = "SHELVED_OFFLOADED"
    SHUTOFF = "SHUTOFF"
    SOFT_DELETED = "SOFT_DELETED"
    STOPPED = "STOPPED"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"
    VERIFY_RESIZE = "VERIFY_RESIZE"


class PowerState(str, Enum):
    """Virtual machine power state enum."""

    NO_STATE = "NO_STATE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    SHUTDOWN = "SHUTDOWN"
    CRASHED = "CRASHED"
    SUSPENDED = "SUSPENDED"


class FirewallProtocol(str, Enum):
    """Firewall protocol enum."""

    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"


class FirewallDirection(str, Enum):
    """Firewall direction enum."""

    INGRESS = "ingress"
    EGRESS = "egress"


class FirewallRule(BaseModel):
    """Firewall rule model."""

    id: int | None = Field(None, description="Rule ID")
    protocol: FirewallProtocol = Field(..., description="Protocol")
    direction: FirewallDirection = Field(..., description="Traffic direction")
    port_range_min: int | None = Field(None, ge=1, le=65535, description="Minimum port")
    port_range_max: int | None = Field(None, ge=1, le=65535, description="Maximum port")
    remote_ip_prefix: str | None = Field(None, description="Remote IP prefix (CIDR)")
    description: str | None = Field(None, description="Rule description")

    @field_validator("remote_ip_prefix")
    @classmethod
    def validate_cidr(cls, v: str | None) -> str | None:
        """Validate CIDR notation."""
        if v and "/" not in v:
            # Add default /32 for single IPs
            return f"{v}/32"
        return v


class VMNetwork(BaseModel):
    """Virtual machine network configuration."""

    id: int = Field(..., description="Network ID")
    name: str = Field(..., description="Network name")
    ip_address: str = Field(..., description="IP address")
    mac_address: str = Field(..., description="MAC address")
    network_type: str = Field(..., description="Network type (public/private)")


class VirtualMachine(BaseResource):
    """Virtual machine model."""

    name: str = Field(..., description="VM name")
    status: VMStatus = Field(..., description="VM status")
    power_state: PowerState = Field(..., description="Power state")
    flavor_id: int = Field(..., description="Flavor ID")
    flavor_name: str = Field(..., description="Flavor name")
    image_id: int | None = Field(None, description="Image ID")
    image_name: str | None = Field(None, description="Image name")
    environment_id: int = Field(..., description="Environment ID")
    environment_name: str = Field(..., description="Environment name")
    key_name: str | None = Field(None, description="SSH key name")
    user_data: str | None = Field(None, description="User data script")
    networks: list[VMNetwork] = Field(
        default_factory=list, description="Network configurations"
    )
    volumes_attached: list[int] = Field(
        default_factory=list, description="Attached volume IDs"
    )
    floating_ips: list[str] = Field(
        default_factory=list, description="Attached floating IPs"
    )
    firewall_rules: list[FirewallRule] = Field(
        default_factory=list, description="Firewall rules"
    )
    tags: list[str] = Field(default_factory=list, description="VM tags")


class CreateVMRequest(BaseModel):
    """Create VM request model."""

    name: str = Field(..., min_length=1, max_length=255, description="VM name")
    environment_id: int = Field(..., description="Environment ID")
    flavor_id: int = Field(..., description="Flavor ID")
    image_id: int | None = Field(None, description="Image ID")
    key_name: str | None = Field(None, description="SSH key name")
    count: int = Field(default=1, ge=1, le=10, description="Number of VMs to create")
    assign_floating_ip: bool = Field(
        default=False, description="Auto-assign floating IP"
    )
    user_data: str | None = Field(None, description="User data script")
    tags: list[str] = Field(default_factory=list, description="VM tags")
    volume_size: int | None = Field(None, ge=1, description="Boot volume size in GB")
    security_groups: list[str] = Field(
        default_factory=list, description="Security group names"
    )


class VMEvent(BaseModel):
    """Virtual machine event model."""

    id: int = Field(..., description="Event ID")
    event_type: str = Field(..., description="Event type")
    message: str = Field(..., description="Event message")
    timestamp: datetime = Field(..., description="Event timestamp")
    severity: str = Field(..., description="Event severity")
    metadata: dict[str, Any] | None = Field(None, description="Event metadata")


class VMActionResponse(BaseModel):
    """Response for VM actions."""

    success: bool = Field(..., description="Action success status")
    message: str = Field(..., description="Action message")
    vm_id: int = Field(..., description="VM ID")
    action: str = Field(..., description="Action performed")
    new_status: VMStatus | None = Field(None, description="New VM status")
