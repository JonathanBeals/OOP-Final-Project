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
            self._environments: dict[str, list[Server]] = {}

    @property
    def servers(self) -> list[Server]:
        """Return the default servers managed by this manager."""
        return self._servers

    def get_environment_servers(
        self,
        environment_id: str
    ) -> list[Server]:
        """Return servers belonging to a specific environment.

        Args:
            environment_id (str): unique environment identifier

        Returns:
            list[Server]: servers belonging to the environment
        """
        if environment_id not in self._environments:
            self._environments[environment_id] = []

        return self._environments[environment_id]

    def clear_environment(self, environment_id: str) -> None:
        """Remove one environment and its simulated state.

        Args:
            environment_id (str): environment to remove
        """
        self._environments.pop(environment_id, None)

    def clear_all_environments(self) -> None:
        """Remove all session environments."""
        self._environments.clear()

    def add_server(
        self,
        server: Server,
        environment_id: str | None = None
    ) -> None:
        """Add a server to the manager.

        Args:
            server (Server): server to add
            environment_id (str | None): optional environment identifier
        """
        if environment_id is None:
            self._servers.append(server)
        else:
            self.get_environment_servers(
                environment_id
            ).append(server)

    def get_server(
        self,
        server_id: int,
        environment_id: str | None = None
    ) -> Server | None:
        """Find a server by ID.

        Args:
            server_id (int): server ID to search for
            environment_id (str | None): optional environment identifier

        Returns:
            Server | None: matching server or None
        """
        servers = (
            self._servers
            if environment_id is None
            else self.get_environment_servers(environment_id)
        )

        for server in servers:
            if server.server_id == server_id:
                return server

        return None

    def get_virtual_machine(
        self,
        vm_id: int,
        environment_id: str | None = None
    ) -> VirtualMachine | None:
        """Find a virtual machine across servers.

        Args:
            vm_id (int): virtual machine ID
            environment_id (str | None): optional environment identifier

        Returns:
            VirtualMachine | None: matching VM or None
        """
        servers = (
            self._servers
            if environment_id is None
            else self.get_environment_servers(environment_id)
        )

        for server in servers:
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
        host: str,
        environment_id: str | None = None
    ) -> VirtualMachine | None:
        """Create a VM and add it to a server.

        Args:
            server_id (int): server that will host the VM
            vm_id (int): unique VM ID
            name (str): VM name
            status (str): initial VM status
            host (str): VM host name
            environment_id (str | None): optional environment identifier

        Returns:
            VirtualMachine | None: created VM or None
        """
        server = self.get_server(
            server_id,
            environment_id
        )

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

    def start_vm(
        self,
        vm_id: int,
        environment_id: str | None = None
    ) -> bool:
        """Start a virtual machine.

        Args:
            vm_id (int): VM ID
            environment_id (str | None): optional environment identifier

        Returns:
            bool: True if VM was found and started
        """
        virtual_machine = self.get_virtual_machine(
            vm_id,
            environment_id
        )

        if virtual_machine is None:
            return False

        virtual_machine.status = "running"

        return True

    def stop_vm(
        self,
        vm_id: int,
        environment_id: str | None = None
    ) -> bool:
        """Stop a virtual machine.

        Args:
            vm_id (int): VM ID
            environment_id (str | None): optional environment identifier

        Returns:
            bool: True if VM was found and stopped
        """
        virtual_machine = self.get_virtual_machine(
            vm_id,
            environment_id
        )

        if virtual_machine is None:
            return False

        virtual_machine.status = "stopped"

        return True

    def delete_vm(
        self,
        vm_id: int,
        environment_id: str | None = None
    ) -> bool:
        """Delete a virtual machine.

        Args:
            vm_id (int): VM ID
            environment_id (str | None): optional environment identifier

        Returns:
            bool: True if VM was found and removed
        """
        servers = (
            self._servers
            if environment_id is None
            else self.get_environment_servers(environment_id)
        )

        for server in servers:
            for virtual_machine in server.virtual_machines:
                if virtual_machine.vm_id == vm_id:
                    server.remove_virtual_machine(vm_id)
                    return True

        return False
