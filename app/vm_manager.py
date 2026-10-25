"""Manager for servers and virtual machines.

Provides a single facade for creating and managing virtual machines
across simulated servers.
"""

from app.server import Server
from app.virtual_machine import VirtualMachine
from app.vm_factory import VmFactory


class VMManager:
    """Singleton facade for managing servers and virtual machines."""

    _instance: "VMManager | None" = None

    def __new__(cls) -> "VMManager":
        """Return the single VMManager instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        """Initialize the manager once."""
        if not hasattr(self, "_servers"):
            self._servers: list[Server] = []

    @property
    def servers(self) -> list[Server]:
        """Return the servers managed by this manager."""
        return self._servers

    def add_server(self, server: Server) -> None:
        """Add a server to the manager.

        Args:
            server (Server): server to add
        """
        self._servers.append(server)

    def get_server(self, server_id: int) -> Server | None:
        """Find a server by ID.

        Args:
            server_id (int): server ID to search for

        Returns:
            Server | None: matching server or None
        """
        for server in self._servers:
            if server.server_id == server_id:
                return server

        return None

    def get_virtual_machine(self, vm_id: int) -> VirtualMachine | None:
        """Find a virtual machine across all servers.

        Args:
            vm_id (int): virtual machine ID

        Returns:
            VirtualMachine | None: matching VM or None
        """
        for server in self._servers:
            for virtual_machine in server.virtual_machines:
                if virtual_machine.vm_id == vm_id:
                    return virtual_machine

        return None

    def create_vm(
        self,
        server_id: int,
        vm_id: int,
        name: str,
        status: str,
        host: str
    ) -> VirtualMachine | None:
        """Create a VM and add it to a server.

        Args:
            server_id (int): server that will host the VM
            vm_id (int): unique VM ID
            name (str): VM name
            status (str): initial VM status
            host (str): VM host name

        Returns:
            VirtualMachine | None: created VM or None if server is not found
        """
        server = self.get_server(server_id)

        if server is None:
            return None

        virtual_machine = VmFactory.create_vm(
            vm_id,
            name,
            status,
            host
        )

        server.add_virtual_machine(virtual_machine)

        return virtual_machine

    def start_vm(self, vm_id: int) -> bool:
        """Start a virtual machine.

        Args:
            vm_id (int): VM ID

        Returns:
            bool: True if VM was found and started
        """
        virtual_machine = self.get_virtual_machine(vm_id)

        if virtual_machine is None:
            return False

        virtual_machine.status = "running"

        return True

    def stop_vm(self, vm_id: int) -> bool:
        """Stop a virtual machine.

        Args:
            vm_id (int): VM ID

        Returns:
            bool: True if VM was found and stopped
        """
        virtual_machine = self.get_virtual_machine(vm_id)

        if virtual_machine is None:
            return False

        virtual_machine.status = "stopped"

        return True

    def delete_vm(self, vm_id: int) -> bool:
        """Delete a virtual machine.

        Args:
            vm_id (int): VM ID

        Returns:
            bool: True if VM was found and removed
        """
        for server in self._servers:
            for virtual_machine in server.virtual_machines:
                if virtual_machine.vm_id == vm_id:
                    server.remove_virtual_machine(vm_id)
                    return True

        return False
