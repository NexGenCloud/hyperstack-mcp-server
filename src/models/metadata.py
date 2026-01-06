"""Metadata models for Hyperstack MCP Server."""

from pydantic import BaseModel, Field


class Flavor(BaseModel):
    """Flavor (instance type) model."""

    id: int = Field(..., description="Flavor ID")
    name: str = Field(..., description="Flavor name")
    vcpus: int = Field(..., description="Number of vCPUs")
    ram: int = Field(..., description="RAM in MB")
    disk: int = Field(..., description="Disk size in GB")
    gpu_count: int | None = Field(None, description="Number of GPUs")
    gpu_type: str | None = Field(None, description="GPU type/model")
    price_per_hour: float = Field(..., description="Price per hour")
    region: str = Field(..., description="Available region")
    availability: str = Field(..., description="Availability status")
    network_speed: str | None = Field(None, description="Network speed")
    ephemeral: int | None = Field(None, description="Ephemeral storage in GB")
    public: bool = Field(default=True, description="Is publicly available")
    description: str | None = Field(None, description="Flavor description")


class Environment(BaseModel):
    """Environment (region/location) model."""

    id: int = Field(..., description="Environment ID")
    name: str = Field(..., description="Environment name")
    region: str = Field(..., description="Region code")
    country: str = Field(..., description="Country")
    city: str = Field(..., description="City")
    availability_zones: list[str] = Field(
        default_factory=list, description="Available zones"
    )
    features: list[str] = Field(default_factory=list, description="Supported features")
    status: str = Field(..., description="Environment status")
    description: str | None = Field(None, description="Environment description")


class StockAvailability(BaseModel):
    """Stock availability model."""

    flavor_id: int = Field(..., description="Flavor ID")
    flavor_name: str = Field(..., description="Flavor name")
    region: str = Field(..., description="Region")
    available_count: int = Field(..., description="Available instance count")
    total_count: int = Field(..., description="Total instance count")
    availability_percentage: float = Field(..., description="Availability percentage")
    status: str = Field(
        ..., description="Stock status (available/limited/out_of_stock)"
    )
    last_updated: str = Field(..., description="Last update timestamp")
    estimated_restock: str | None = Field(None, description="Estimated restock time")


class StockCheckRequest(BaseModel):
    """Stock check request model."""

    flavor: str = Field(..., description="Flavor name or ID")
    region: str | None = Field(None, description="Specific region to check")
    count: int = Field(default=1, ge=1, description="Number of instances needed")


class FlavorFilter(BaseModel):
    """Flavor filter parameters."""

    region: str | None = Field(None, description="Filter by region")
    min_vcpus: int | None = Field(None, ge=1, description="Minimum vCPUs")
    max_vcpus: int | None = Field(None, description="Maximum vCPUs")
    min_ram: int | None = Field(None, ge=512, description="Minimum RAM in MB")
    max_ram: int | None = Field(None, description="Maximum RAM in MB")
    min_disk: int | None = Field(None, ge=1, description="Minimum disk in GB")
    max_disk: int | None = Field(None, description="Maximum disk in GB")
    gpu_required: bool | None = Field(None, description="GPU required")
    gpu_type: str | None = Field(None, description="Specific GPU type")
    max_price: float | None = Field(None, description="Maximum price per hour")
