"""virtual machine model for the VM management system
"""


class VirtualMachine:
    """class for Virtual machine
    """
    def __init__(self, vm_id: int, name: str, status: str, host: str) -> None:
        """initializes virtual machine class

        Args:
            vm_id (int): unique id for virtual machine
            name (str): name of the virtual machine
            status (str): status of the virtual machine
            host (str): host server for the virtual machine
        """
        self._vm_id = vm_id
        self._name = name
        self._status = status
        self._host = host

    @property
    def vm_id(self) -> int:
        """getter for vm_id

        Returns:
            int: the virtual machine ID
        """
        return self._vm_id

    @property
    def name(self) -> str:
        """getter for name

        Returns:
            str: the name for the virtual machine
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """setter for name

        Args:
            name (str): new name for the virtual machine
        """
        self._name = name

    @property
    def status(self) -> str:
        """getter for status

        Returns:
            str: the status of the virtual machine
        """
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        """setter for status

        Args:
            status (str): new status of the virtual machine

        """
        self._status = status

    @property
    def host(self) -> str:
        """getter for host

        Returns:
            str: the host server of the virtual machine
        """
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        """setter for host

        Args:
            host (str): new host server of the virtual machine
        """
        self._host = host
