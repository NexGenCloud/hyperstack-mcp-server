"""Cluster handlers for MCP actions."""

from typing import Any

from src.mcp_instance import mcp
from src.models.clusters import ClusterType, CreateClusterRequest

from .base import BaseHandler

handler = BaseHandler()


@mcp.tool(
    name="create_cluster", title="Create Cluster", description="Create a new cluster"
)
async def create_cluster(
    name: str,
    environment_id: int,
    master_flavor_id: int,
    worker_flavor_id: int,
    cluster_type: str = "kubernetes",
    version: str = "1.28.0",
    master_count: int = 1,
    worker_count: int = 2,
    network_id: int | None = None,
    subnet_cidr: str = "10.0.0.0/16",
    service_cidr: str | None = "10.96.0.0/12",
    pod_cidr: str | None = "10.244.0.0/16",
    key_name: str | None = None,
    dns_enabled: bool = True,
    ingress_enabled: bool = False,
    monitoring_enabled: bool = False,
    autoscaling_enabled: bool = False,
    min_nodes: int | None = None,
    max_nodes: int | None = None,
) -> dict[str, Any]:
    """Create a new cluster."""
    request = CreateClusterRequest(
        name=name,
        cluster_type=ClusterType(cluster_type),
        version=version,
        environment_id=environment_id,
        master_count=master_count,
        worker_count=worker_count,
        master_flavor_id=master_flavor_id,
        worker_flavor_id=worker_flavor_id,
        network_id=network_id,
        subnet_cidr=subnet_cidr,
        service_cidr=service_cidr,
        pod_cidr=pod_cidr,
        key_name=key_name,
        dns_enabled=dns_enabled,
        ingress_enabled=ingress_enabled,
        monitoring_enabled=monitoring_enabled,
        autoscaling_enabled=autoscaling_enabled,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
    )

    response = await handler.client.create_cluster(
        **request.model_dump(exclude_none=True)
    )
    validated = await handler.validate_response(response, "create_cluster")

    return handler.format_success_response(
        f"Cluster '{name}' creation initiated successfully",
        data=validated,
    )


@mcp.tool(name="list_clusters", title="List Clusters", description="List all clusters")
async def list_clusters(
    page: int | None = None,
    page_size: int | None = None,
) -> dict[str, Any]:
    """List all clusters."""
    response = await handler.client.list_clusters(
        page=page,
        page_size=page_size,
    )

    validated = await handler.validate_response(response, "list_clusters")

    return handler.format_list_response(
        items=validated.get("results", []),
        total=validated.get("count"),
        page=page,
        page_size=page_size,
    )


@mcp.tool(
    name="get_cluster", title="Get Cluster Details", description="Get cluster details"
)
async def get_cluster(cluster_id: int) -> dict[str, Any]:
    """Get cluster details."""
    response = await handler.client.get_cluster(cluster_id)
    validated = await handler.validate_response(response, "get_cluster")

    return handler.format_success_response(
        f"Retrieved details for cluster {cluster_id}",
        data=validated,
    )


@mcp.tool(name="delete_cluster", title="Delete Cluster", description="Delete a cluster")
async def delete_cluster(cluster_id: int) -> dict[str, Any]:
    """Delete a cluster."""
    response = await handler.client.delete_cluster(cluster_id)
    await handler.validate_response(response, "delete_cluster")

    return handler.format_success_response(
        f"Cluster {cluster_id} deletion initiated successfully",
        cluster_id=cluster_id,
        action="delete",
    )


@mcp.tool(
    name="get_cluster_events",
    title="Get Cluster Events",
    description="Get cluster events",
)
async def get_cluster_events(cluster_id: int) -> dict[str, Any]:
    """Get cluster events."""
    response = await handler.client.get_cluster_events(cluster_id)
    validated = await handler.validate_response(response, "get_cluster_events")

    events = validated.get("events", [])
    return handler.format_list_response(
        items=events,
        total=len(events),
    )
