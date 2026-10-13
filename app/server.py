"""server model for the VM management system
"""

from app.virtual_machine import VirtualMachine


class Server:
    """class for server
    """

    def __init__(
        self,
        server_id: int,
        name: str,
        status: str,
        address: str
    ) -> None:
        """initializes server class

        Args:
            server_id (int): unique id for server
            name (str): name of the server
            status (str): current status of the server
            address (str): network address of the server
        """
        self._server_id = server_id
        self._name = name
        self._status = status
        self._address = address
        self._virtual_machines: list[VirtualMachine] = []

    @property
    def server_id(self) -> int:
        """getter for server id

        Returns:
            int: the server id
        """
        return self._server_id

    @property
    def name(self) -> str:
        """getter for server name

        Returns:
            str: the server name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """setter for server name

        Args:
            name (str): new server name
        """
        self._name = name

    @property
    def status(self) -> str:
        """getter for server status

        Returns:
            str: the server status
        """
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        """setter for server status

        Args:
            status (str): new server status
        """
        self._status = status

    @property
    def address(self) -> str:
        """getter for server address

        Returns:
            str: the server address
        """
        return self._address

    @address.setter
    def address(self, address: str) -> None:
        """setter for server address

        Args:
            address (str): new server address
        """
        self._address = address

    @property
    def virtual_machines(self) -> list[VirtualMachine]:
        """getter for virtual machines

        Returns:
            list[VirtualMachine]: virtual machines hosted by the server
        """
        return self._virtual_machines

    def add_virtual_machine(self, virtual_machine: VirtualMachine) -> None:
        """adds a virtual machine to the server

        Args:
            virtual_machine (VirtualMachine): virtual machine to add
        """
        self._virtual_machines.append(virtual_machine)

    def remove_virtual_machine(self, vm_id: int) -> None:
        """removes a virtual machine from the server

        Args:
            vm_id (int): id of the virtual machine to remove
        """
        self._virtual_machines = [
            vm for vm in self._virtual_machines
            if vm.vm_id != vm_id
        ]