"""Cluster models for Hyperstack MCP Server."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .base import BaseResource


class ClusterStatus(str, Enum):
    """Cluster status enum."""

    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    ERROR = "ERROR"
    DELETING = "DELETING"
    DELETED = "DELETED"
    UPDATING = "UPDATING"
    MAINTENANCE = "MAINTENANCE"


class ClusterType(str, Enum):
    """Cluster type enum."""

    KUBERNETES = "kubernetes"
    DOCKER_SWARM = "docker_swarm"
    NOMAD = "nomad"
    CUSTOM = "custom"


class NodeStatus(str, Enum):
    """Cluster node status enum."""

    READY = "Ready"
    NOT_READY = "NotReady"
    UNKNOWN = "Unknown"
    SCHEDULING_DISABLED = "SchedulingDisabled"


class ClusterNode(BaseModel):
    """Cluster node model."""

    id: int = Field(..., description="Node ID")
    name: str = Field(..., description="Node name")
    role: str = Field(..., description="Node role (master/worker)")
    status: NodeStatus = Field(..., description="Node status")
    vm_id: int = Field(..., description="Underlying VM ID")
    private_ip: str = Field(..., description="Private IP address")
    public_ip: str | None = Field(None, description="Public IP address")
    labels: dict[str, str] = Field(default_factory=dict, description="Node labels")
    taints: list[str] = Field(default_factory=list, description="Node taints")


class Cluster(BaseResource):
    """Cluster model."""

    name: str = Field(..., description="Cluster name")
    cluster_type: ClusterType = Field(..., description="Cluster type")
    status: ClusterStatus = Field(..., description="Cluster status")
    version: str = Field(..., description="Cluster version")
    environment_id: int = Field(..., description="Environment ID")
    environment_name: str = Field(..., description="Environment name")
    master_count: int = Field(..., description="Number of master nodes")
    worker_count: int = Field(..., description="Number of worker nodes")
    nodes: list[ClusterNode] = Field(default_factory=list, description="Cluster nodes")
    api_endpoint: str | None = Field(None, description="API endpoint URL")
    dashboard_url: str | None = Field(None, description="Dashboard URL")
    kubeconfig: str | None = Field(None, description="Kubeconfig content")
    network_id: int = Field(..., description="Network ID")
    subnet_cidr: str = Field(..., description="Subnet CIDR")
    service_cidr: str | None = Field(None, description="Service CIDR")
    pod_cidr: str | None = Field(None, description="Pod CIDR")
    dns_enabled: bool = Field(default=True, description="DNS enabled")
    ingress_enabled: bool = Field(
        default=False, description="Ingress controller enabled"
    )
    monitoring_enabled: bool = Field(default=False, description="Monitoring enabled")
    autoscaling_enabled: bool = Field(default=False, description="Autoscaling enabled")
    min_nodes: int | None = Field(None, description="Minimum nodes for autoscaling")
    max_nodes: int | None = Field(None, description="Maximum nodes for autoscaling")
    tags: list[str] = Field(default_factory=list, description="Cluster tags")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class CreateClusterRequest(BaseModel):
    """Create cluster request model."""

    name: str = Field(..., min_length=1, max_length=255, description="Cluster name")
    cluster_type: ClusterType = Field(
        default=ClusterType.KUBERNETES, description="Cluster type"
    )
    version: str = Field(..., description="Cluster version (e.g., 1.28.0)")
    environment_id: int = Field(..., description="Environment ID")
    master_count: int = Field(
        default=1, ge=1, le=5, description="Number of master nodes"
    )
    worker_count: int = Field(
        default=2, ge=0, le=100, description="Number of worker nodes"
    )
    master_flavor_id: int = Field(..., description="Master node flavor ID")
    worker_flavor_id: int = Field(..., description="Worker node flavor ID")
    network_id: int | None = Field(None, description="Network ID")
    subnet_cidr: str = Field(default="10.0.0.0/16", description="Subnet CIDR")
    service_cidr: str | None = Field("10.96.0.0/12", description="Service CIDR")
    pod_cidr: str | None = Field("10.244.0.0/16", description="Pod CIDR")
    key_name: str | None = Field(None, description="SSH key name")
    dns_enabled: bool = Field(default=True, description="Enable DNS")
    ingress_enabled: bool = Field(
        default=False, description="Enable ingress controller"
    )
    monitoring_enabled: bool = Field(default=False, description="Enable monitoring")
    autoscaling_enabled: bool = Field(default=False, description="Enable autoscaling")
    min_nodes: int | None = Field(
        None, ge=0, description="Minimum nodes for autoscaling"
    )
    max_nodes: int | None = Field(
        None, ge=1, description="Maximum nodes for autoscaling"
    )
    tags: list[str] = Field(default_factory=list, description="Cluster tags")


class ClusterEvent(BaseModel):
    """Cluster event model."""

    id: int = Field(..., description="Event ID")
    cluster_id: int = Field(..., description="Cluster ID")
    event_type: str = Field(..., description="Event type")
    message: str = Field(..., description="Event message")
    timestamp: str = Field(..., description="Event timestamp")
    severity: str = Field(..., description="Event severity")
    component: str | None = Field(
        None, description="Component that generated the event"
    )
    node_id: int | None = Field(None, description="Related node ID")
    metadata: dict[str, Any] | None = Field(None, description="Event metadata")


class ClusterActionResponse(BaseModel):
    """Response for cluster actions."""

    success: bool = Field(..., description="Action success status")
    message: str = Field(..., description="Action message")
    cluster_id: int = Field(..., description="Cluster ID")
    action: str = Field(..., description="Action performed")
    new_status: ClusterStatus | None = Field(None, description="New cluster status")
