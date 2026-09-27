"""virtual machine model for the VM managment system
"""


class VirtualMachine:
    """class for Virtual machine
    """
    def __init__(self, vm_id: int, name: str, status: str, host: str) -> None:
        """initializes virtual machine class

        Args:
            vm_id (int): _vm_id
            name (str): _name
            status (str): _status
            host (str): _host
        """
        self._vm_id = vm_id
        self._name = name
        self._status = status
        self._host = host

    @property
    def vm_id(self) -> int:
        """vm_id

        Returns:
            int: _vm_id
        """
        return self._vm_id

    @property
    def name(self) -> str:
        """name

        Returns:
            str: _name
        """
        return self._name

    @property
    def status(self) -> str:
        """status

        Returns:
            str: _status
        """
        return self._status

    @property
    def host(self) -> str:
        """host

        Returns:
            str: _host
        """
        return self._host
