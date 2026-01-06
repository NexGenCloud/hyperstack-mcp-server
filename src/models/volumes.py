"""Volume models for Hyperstack MCP Server."""

from enum import Enum

from pydantic import BaseModel, Field

from .base import BaseResource


class VolumeStatus(str, Enum):
    """Volume status enum."""

    AVAILABLE = "available"
    IN_USE = "in-use"
    CREATING = "creating"
    DELETING = "deleting"
    ERROR = "error"
    ERROR_DELETING = "error_deleting"
    BACKING_UP = "backing-up"
    RESTORING_BACKUP = "restoring-backup"
    ERROR_BACKING_UP = "error_backing-up"
    ERROR_RESTORING = "error_restoring"
    MAINTENANCE = "maintenance"


class VolumeType(str, Enum):
    """Volume type enum."""

    SSD = "ssd"
    HDD = "hdd"
    NVME = "nvme"
    STANDARD = "standard"
    PERFORMANCE = "performance"


class VolumeAttachment(BaseModel):
    """Volume attachment model."""

    id: int = Field(..., description="Attachment ID")
    volume_id: int = Field(..., description="Volume ID")
    vm_id: int = Field(..., description="VM ID")
    device: str = Field(..., description="Device name (e.g., /dev/vdb)")
    attached_at: str = Field(..., description="Attachment timestamp")


class Volume(BaseResource):
    """Volume model."""

    name: str = Field(..., description="Volume name")
    description: str | None = Field(None, description="Volume description")
    size: int = Field(..., gt=0, description="Volume size in GB")
    status: VolumeStatus = Field(..., description="Volume status")
    volume_type: VolumeType = Field(..., description="Volume type")
    bootable: bool = Field(default=False, description="Is bootable volume")
    encrypted: bool = Field(default=False, description="Is encrypted")
    attachments: list[VolumeAttachment] = Field(
        default_factory=list, description="Volume attachments"
    )
    availability_zone: str | None = Field(None, description="Availability zone")
    source_volume_id: int | None = Field(None, description="Source volume ID if cloned")
    snapshot_id: int | None = Field(None, description="Source snapshot ID")
    tags: list[str] = Field(default_factory=list, description="Volume tags")


class CreateVolumeRequest(BaseModel):
    """Create volume request model."""

    name: str = Field(..., min_length=1, max_length=255, description="Volume name")
    size: int = Field(..., ge=1, le=10000, description="Volume size in GB")
    volume_type: VolumeType = Field(default=VolumeType.SSD, description="Volume type")
    description: str | None = Field(
        None, max_length=500, description="Volume description"
    )
    availability_zone: str | None = Field(None, description="Availability zone")
    encrypted: bool = Field(default=False, description="Enable encryption")
    source_volume_id: int | None = Field(None, description="Clone from volume ID")
    snapshot_id: int | None = Field(None, description="Create from snapshot ID")
    tags: list[str] = Field(default_factory=list, description="Volume tags")


class UpdateVolumeRequest(BaseModel):
    """Update volume request model."""

    name: str | None = Field(
        None, min_length=1, max_length=255, description="Volume name"
    )
    description: str | None = Field(
        None, max_length=500, description="Volume description"
    )
    size: int | None = Field(
        None, ge=1, le=10000, description="New size in GB (extend only)"
    )
    tags: list[str] | None = Field(None, description="Volume tags")


class VolumeTypeInfo(BaseModel):
    """Volume type information model."""

    id: int = Field(..., description="Volume type ID")
    name: str = Field(..., description="Volume type name")
    description: str = Field(..., description="Volume type description")
    min_size: int = Field(..., description="Minimum size in GB")
    max_size: int = Field(..., description="Maximum size in GB")
    iops: int | None = Field(None, description="IOPS limit")
    throughput: int | None = Field(None, description="Throughput in MB/s")
    price_per_gb: float = Field(..., description="Price per GB per hour")


class AttachVolumeRequest(BaseModel):
    """Attach volume request model."""

    vm_id: int = Field(..., description="VM ID to attach to")
    device: str | None = Field(
        None, description="Device name (auto-assign if not specified)"
    )


class VolumeActionResponse(BaseModel):
    """Response for volume actions."""

    success: bool = Field(..., description="Action success status")
    message: str = Field(..., description="Action message")
    volume_id: int = Field(..., description="Volume ID")
    action: str = Field(..., description="Action performed")
    new_status: VolumeStatus | None = Field(None, description="New volume status")
