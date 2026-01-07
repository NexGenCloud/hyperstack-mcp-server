"""Virtual Machine models for Hyperstack MCP Server."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class VMStatus(str, Enum):
    """Virtual machine status enum."""

    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    BUILD = "BUILD"
    DELETED = "DELETED"
    ERROR = "ERROR"
    HARD_REBOOT = "HARD_REBOOT"
    PASSWORD = "PASSWORD"  # noqa: S105 - This is a VM status, not a password
    REBOOT = "REBOOT"
    RESIZE = "RESIZE"
    REVERT_RESIZE = "REVERT_RESIZE"
    SHELVED = "SHELVED"
    SHELVED_OFFLOADED = "SHELVED_OFFLOADED"
    SHUTOFF = "SHUTOFF"
    HIBERNATED = "HIBERNATED"
    UNKNOWN = "UNKNOWN"


class PowerState(str, Enum):
    """Virtual machine power state enum."""

    NO_STATE = "NO_STATE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    SHUTDOWN = "SHUTDOWN"
    CRASHED = "CRASHED"
    SUSPENDED = "SUSPENDED"
    NONE = None


class FirewallProtocol(str, Enum):
    """Firewall protocol enum."""

    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"


class FirewallDirection(str, Enum):
    """Firewall direction enum."""

    INGRESS = "ingress"
    EGRESS = "egress"


class FirewallRuleResponse(BaseModel):
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


class VMFeatures(BaseModel):
    network_optimised: bool = Field(..., description="Whether high-speed networking is enabled on the VM.")
    green_status: str = Field(..., description="Sustainability indicator for the VM.")


class Environment(BaseModel):
    id: int = Field(..., description="Environment ID")
    name: str = Field(..., description="Environment name")
    org_id: int = Field(..., description="Organization ID")
    region: str = Field(..., description="Deployment region")
    features: VMFeatures


class FlavorFeatures(BaseModel):
    os: str | None = Field(
        None,
        description="Operating system supported by the flavor"
    )


class Flavor(BaseModel):
    id: int = Field(..., description="Flavor ID")
    name: str = Field(..., description="Flavor name")
    cpu: int = Field(..., description="Number of CPUs")
    ram: float = Field(..., description="RAM size in GB")
    disk: int = Field(..., description="Disk size in GB")
    ephemeral: int = Field(..., description="Ephemeral disk size in GB")
    gpu: str | None = Field(None, description="GPU type")
    gpu_count: int = Field(..., description="Number of GPUs")
    labels: list[dict] = Field(..., description="Flavor labels")
    features: FlavorFeatures


class VolumeAttachment(BaseModel):
    volume: dict[str, int] = Field(..., description="Attached volume information")
    status: str = Field(..., description="Attachment status")
    device: str = Field(..., description="Device name")
    created_at: datetime = Field(..., description="Attachment creation time")


class VirtualMachine(BaseModel):
    """Virtual machine model."""

    id: int = Field(..., description="Virtual machine ID")
    name: str = Field(..., description="Virtual machine name")
    status: str = Field(..., description="VM status")

    environment: Environment
    image: dict[str, str] = Field(..., description="Operating system image information")
    flavor: Flavor
    os: str = Field(..., description="Operating system")

    keypair: dict[str, str] = Field(..., description="SSH keypair information")

    volume_attachments: list[VolumeAttachment]
    security_rules: list[FirewallRuleResponse]

    power_state: str | None = Field(default=None, description="Power state")
    vm_state: str | None = Field(default=None, description="VM lifecycle state")

    fixed_ip: str | None = Field(default=None, description="Private IP address")
    floating_ip: str | None = Field(default=None, description="Public IP address")
    floating_ip_status: str = Field(..., description="Floating IP status")

    callback_url: str | None = Field(default=None, description="Callback URL")
    locked: bool = Field(..., description="VM lock state")

    contract_id: int | None = Field(default=None, description="Billing contract ID")
    labels: list[str] = Field(..., description="VM labels")
    created_at: datetime = Field(..., description="Creation timestamp")

    features: VMFeatures

    is_snapshotting: bool = Field(..., description="Snapshot operation in progress")

    cluster_id: int | None = Field(None, description="Associated Kubernetes cluster ID")

    port_randomization: bool = Field(..., description="Random public port assignment enabled")
    port_randomization_status: str = Field(..., description="Port randomization status")

    requires_public_ip: bool = Field(..., description="Requires floating IP")


class FirewallRuleRequest(BaseModel):
    """Firewall rule request model."""

    direction: FirewallDirection = Field(..., description="Direction of the rule")
    protocol: str = Field(..., description="Protocol")
    ethertype: str = Field(..., description="Ether type")
    remote_ip_prefix: str = Field(..., description="Remote IP prefix (CIDR)")
    port_range_min: int | None = Field(None, description="Minimum port")
    port_range_max: int | None = Field(None, description="Maximum port")


class Profile(BaseModel):
    """Profile model."""

    name: str = Field(..., description="Profile name")
    description: str = Field(..., description="Profile description")


class VMEvent(BaseModel):
    """Virtual machine event model."""

    id: int = Field(..., description="Event ID")
    event_type: str = Field(..., description="Event type")
    message: str = Field(..., description="Event message")
    timestamp: datetime = Field(..., description="Event timestamp")
    severity: str = Field(..., description="Event severity")
    metadata: dict[str, Any] | None = Field(None, description="Event metadata")


class CreateVMRequest(BaseModel):
    """Create VM request model."""

    name: str = Field(..., description="VM name")
    environment_name: str = Field(..., description="Environment name")
    image_name: str = Field(..., description="Image name")
    flavor_name: str = Field(..., description="Flavor name")
    key_name: str = Field(..., description="SSH key name")
    count: int = Field(..., description="Number of VMs to create")
    assign_floating_ip: bool | None = Field(False, description="Assign floating IP")
    enable_port_randomization: bool | None = Field(True, description="Enable port randomization")
    security_rules: list[FirewallRuleRequest] | None = Field(default_factory=list, description="Security rules")
    create_bootable_volume: bool | None = Field(False, description="Create bootable volume")
    user_data: str | None = Field(None, description="User data script")
    callback_url: str | None = Field(None, description="Callback URL")
    profile: Profile | None = Field(None, description="Profile")
    labels: list[str] | None = Field(default_factory=list, description="Labels")
    contract_id: int | None = Field(None, description="Contract ID")


class ListVMsRequest(BaseModel):
    """List VMs request model."""

    search: int | str | None = Field(default=None, description="Search by VM ID or name")
    environment: int | str | None = Field(default=None, description="Filter by environment")
    page: int | None = Field(default=None, description="Page number")
    pageSize: int | None = Field(default=None, description="Page size")


class GetVMRequest(BaseModel):
    """Get VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to get")


class DeleteVMRequest(BaseModel):
    """Delete VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to delete")


class StartVMRequest(BaseModel):
    """Start VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to start")


class StopVMRequest(BaseModel):
    """Stop VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to stop")


class HibernateVMRequest(BaseModel):
    """Hibernate VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to hibernate")
    retain_ip: bool | None = Field(default=False)


class RestoreVMRequest(BaseModel):
    """Restore VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to restore")


class HardRebootVMRequest(BaseModel):
    """Hard reboot VM request model."""

    vm_id: str = Field(..., description="The ID of the VM to hard reboot")


class AddFirewallRuleRequest(BaseModel):
    """Add firewall rule request model."""

    vm_id: str = Field(..., description="The ID of the VM to add a firewall rule to")
    security_rule: FirewallRuleRequest


class RemoveFirewallRuleRequest(BaseModel):
    """Remove firewall rule request model."""

    vm_id: str = Field(..., description="The ID of the VM to remove a firewall rule from")
    rule_id: str


class AttachPublicIPRequest(BaseModel):
    """Attach public IP request model."""

    vm_id: str = Field(..., description="The ID of the VM to attach a public IP to")



class DetachPublicIPRequest(BaseModel):
    """Detach public IP request model."""

    vm_id: str = Field(..., description="The ID of the VM to detach a public IP from")


class GetVMEventsRequest(BaseModel):
    """Get VM events request model."""

    vm_id: str = Field(..., description="The ID of the VM to get events for")


class AttachVolumeRequest(BaseModel):
    """Attach volume request model."""

    vm_id: str = Field(..., description="The ID of the VM to attach a volume to")
    volume_ids: list[int]


class DetachVolumeRequest(BaseModel):
    """Detach volume request model."""

    vm_id: str = Field(..., description="The ID of the VM to detach a volume from")
    volume_ids: list[int]

# Response Schemas

class VMActionResponse(BaseModel):
    """Response for VM actions."""

    success: bool = Field(..., description="Action success status")
    message: str = Field(..., description="Action message")
    vm_id: int = Field(..., description="VM ID")
    action: str = Field(..., description="Action performed")
    new_status: VMStatus | None = Field(None, description="New VM status")


class CreateVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to create virtual machines. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the request")
    instances: list[VirtualMachine] = Field(..., description="Details of the virtual machines created by the request.")


class ListVMsResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to create virtual machines. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the request")
    page: int | None = Field(
        default=None,
        description="Current page number for the virtual machines listed"
    )
    page_size: int | None = Field(
        default=None,
        description="Number of items per page retrieved"
    )
    count: int | None = Field(
        default=None,
        description="Total number of virtual machine instances returned in the response"
    )
    instances: list[VirtualMachine] = Field(..., description="Details of the virtual machines created by the request.")


class DeleteVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to delete a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the delete request")


class GetVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to get a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the get request")
    instance: VirtualMachine = Field(..., description="Details of the virtual machine retrieved by the request.")


class StartVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to start a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the start request")


class StopVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to stop a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the stop request")


class HibernateVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to hibernate a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the hibernate request")


class HardRebootVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to hard reset a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the hard reset request")


class RestoreVMResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to restore a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the restore request")


class AddFirewallRuleResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to add a firewall rule. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the add firewall rule request")


class RemoveFirewallRuleResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to remove a firewall rule. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the remove firewall rule request")


class AttachPublicIPResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to attach a public IP to a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the attach public IP request")


class DetachPublicIPResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to detach a public IP from a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the detach public IP request")


class GetVMEventsResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to get a virtual machine event. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the get VM event request")


class AttachVolumeResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to attach a volume to a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the attach volume request")


class DetachVolumeResponse(BaseModel):
    status: bool = Field(
        ...,
        description="Indicates the result of the request to detach a volume from a virtual machine. true signifies success, while false indicates an error."
    )
    message: str = Field(..., description="A message describing the result of the detach volume request")
