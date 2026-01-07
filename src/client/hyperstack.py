"""Hyperstack API client implementation."""

from typing import Any, Optional

import structlog

from src.config import settings

from .base import BaseAsyncClient

logger = structlog.get_logger()

# Global client instance
_client: Optional["HyperstackClient"] = None


class HyperstackClient(BaseAsyncClient):
    """Hyperstack API client."""

    def __init__(self) -> None:
        """Initialize Hyperstack client."""
        super().__init__(
            base_url=str(settings.hyperstack_api_url),
            headers=settings.get_auth_headers(),
            timeout=settings.request_timeout,
            max_retries=settings.max_retries,
        )

    # Virtual Machines endpoints
    async def create_vm(self, payload: dict) -> dict[str, Any]:
        """Create a new virtual machine."""
        return await self.post("/core/virtual-machines", json_data=payload)

    async def list_vms(
        self,
        page: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
        environment: str | None = None,
    ) -> dict[str, Any]:
        """List virtual machines."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if search:
            params["search"] = search
        if environment:
            params["environment"] = environment

        return await self.get("/core/virtual-machines", params=params)

    async def get_vm(self, vm_id: int) -> dict[str, Any]:
        """Get virtual machine details."""
        return await self.get(f"/core/virtual-machines/{vm_id}")

    async def delete_vm(self, vm_id: int) -> dict[str, Any]:
        """Delete a virtual machine."""
        return await self.delete(f"/core/virtual-machines/{vm_id}")

    async def start_vm(self, vm_id: int) -> dict[str, Any]:
        """Start a virtual machine."""
        return await self.get(f"/core/virtual-machines/{vm_id}/start")

    async def stop_vm(self, vm_id: int) -> dict[str, Any]:
        """Stop a virtual machine."""
        return await self.get(f"/core/virtual-machines/{vm_id}/stop")

    async def hard_reboot_vm(self, vm_id: int) -> dict[str, Any]:
        """Hard reboot a virtual machine."""
        return await self.get(f"/core/virtual-machines/{vm_id}/hard-reboot")

    async def hibernate_vm(self, vm_id: int, retain_ip: bool = False) -> dict[str, Any]:
        """Hibernate a virtual machine."""
        return await self.get(
            f"/core/virtual-machines/{vm_id}/hibernate", params={"retain_ip": retain_ip}
        )

    async def restore_vm(self, vm_id: int) -> dict[str, Any]:
        """Restore a hibernated virtual machine."""
        return await self.get(f"/core/virtual-machines/{vm_id}/hibernate-restore")

    async def attach_volume_to_vm(
        self, vm_id: int, volume_ids: list[int]
    ) -> dict[str, Any]:
        """Attach a volume to a virtual machine."""
        return await self.post(
            f"/core/virtual-machines/{vm_id}/attach-volumes",
            json_data={"volume_ids": volume_ids},
        )

    async def detach_volume_from_vm(
        self, vm_id: int, volume_ids: list[int]
    ) -> dict[str, Any]:
        """Detach a volume from a virtual machine."""
        return await self.post(
            f"/core/virtual-machines/{vm_id}/detach-volumes",
            json_data={"volume_ids": volume_ids},
        )

    async def attach_floating_ip_to_vm(self, vm_id: int) -> dict[str, Any]:
        """Attach a floating IP to a virtual machine."""
        return await self.post(f"/core/virtual-machines/{vm_id}/attach-floatingip")

    async def detach_floating_ip_from_vm(self, vm_id: int) -> dict[str, Any]:
        """Detach a floating IP from a virtual machine."""
        return await self.post(f"/core/virtual-machines/{vm_id}/detach-floatingip")

    async def add_firewall_rule(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Add a firewall rule to a virtual machine."""
        vm_id = payload.pop("vm_id")
        security_rules = payload["security_rule"]
        return await self.post(
            f"/core/virtual-machines/{vm_id}/sg-rules",
            json_data=security_rules,
        )

    async def remove_firewall_rule(self, vm_id: int, rule_id: int) -> dict[str, Any]:
        """Remove a firewall rule from a virtual machine."""
        return await self.delete(f"/core/virtual-machines/{vm_id}/sg-rules/{rule_id}")

    async def get_vm_events(self, vm_id: int) -> dict[str, Any]:
        """Get virtual machine events."""
        return await self.get(f"/core/virtual-machines/{vm_id}/events")

    # Volumes endpoints
    async def create_volume(self, payload: dict) -> dict[str, Any]:
        """Create a new volume."""
        return await self.post("/core/volumes", json_data=payload)

    async def list_volumes(
        self,
        page: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """List volumes."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if search:
            params["search"] = search

        return await self.get("/core/volumes", params=params)

    async def get_volume(self, volume_id: int) -> dict[str, Any]:
        """Get volume details."""
        return await self.get(f"/core/volumes/{volume_id}")

    async def update_volume(self, volume_id: int, payload: dict) -> dict[str, Any]:
        """Update a volume."""
        return await self.put(f"/core/volumes/{volume_id}", json_data=payload)

    async def delete_volume(self, volume_id: int) -> dict[str, Any]:
        """Delete a volume."""
        return await self.delete(f"/core/volumes/{volume_id}")

    async def list_volume_types(self) -> dict[str, Any]:
        """List available volume types."""
        return await self.get("/core/volume-types")

    async def update_volume_attachment(
        self, volume_attachment_id: int, attachment_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update volume attachment."""
        return await self.patch(
            f"/core/volume-attachment/{volume_attachment_id}",
            json_data=attachment_data,
        )

    # Metadata endpoints
    async def list_flavors(self, region: str | None = None) -> dict[str, Any]:
        """List available flavors."""
        params: dict[str, Any] = {}
        if region:
            params["region"] = region

        return await self.get("/core/flavors", params=params)

    async def list_environments(
        self,
        page: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """List available environments."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if search:
            params["search"] = search

        return await self.get("/core/environments", params=params)

    async def get_environment(self, environment_id: int) -> dict[str, Any]:
        """Get environment details."""
        return await self.get(f"/core/environments/{environment_id}")

    async def check_stocks(self) -> dict[str, Any]:
        """Check stock availability for a flavor."""
        return await self.get("/core/stocks")

    # Clusters endpoints
    async def create_cluster(self, payload: dict) -> dict[str, Any]:
        """Create a new cluster."""
        return await self.post("/core/clusters", json_data=payload)

    async def list_clusters(
        self,
        search: str | None = None,
        environment: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """List clusters."""
        params: dict[str, Any] = {}
        if search is not None:
            params["search"] = search
        if environment is not None:
            params["environment"] = environment
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        return await self.get("/core/clusters", params=params)

    async def get_cluster(self, cluster_id: int) -> dict[str, Any]:
        """Get cluster details."""
        return await self.get(f"/core/clusters/{cluster_id}")

    async def delete_cluster(self, cluster_id: int) -> dict[str, Any]:
        """Delete a cluster."""
        return await self.delete(f"/core/clusters/{cluster_id}")

    async def get_cluster_events(self, cluster_id: int) -> dict[str, Any]:
        """Get cluster events."""
        return await self.get(f"/core/clusters/{cluster_id}/events")

    # Billing endpoints
    async def get_billing_status(self) -> dict[str, Any]:
        """Get billing status."""
        return await self.get("/billing/alive")

    async def get_billing_usage(
        self,
        deleted: str | None = None,
        environment: str | None = None,
    ) -> dict[str, Any]:
        """Get billing usage."""
        params: dict[str, Any] = {}
        if deleted:
            params["start_date"] = deleted
        if environment:
            params["end_date"] = environment

        return await self.get("/billing/billing/usage", params=params)

    async def get_previous_day_cost(self) -> dict[str, Any]:
        """Get previous day cost."""
        return await self.get("/billing/billing/last-day-cost")

    async def get_credit_balance(self) -> dict[str, Any]:
        """Get credit balance."""
        return await self.get("/billing/user-credit/credit")

    async def get_payment_history(self) -> dict[str, Any]:
        """Get payment history."""
        return await self.get("/billing/payment/payment-details")


def get_client() -> HyperstackClient:
    """Get or create Hyperstack client singleton."""
    global _client  # noqa: PLW0603 - Global singleton pattern is intentional
    if _client is None:
        _client = HyperstackClient()
    return _client


async def initialize_client() -> HyperstackClient:
    """Initialize and connect the client."""
    client = get_client()
    await client.connect()
    return client
