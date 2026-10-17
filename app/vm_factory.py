"""Place where the fake virtual machines are created
"""

from app.virtual_machine import VirtualMachine


class VmFactory:
    """factory for creating VirtualMachine objects
    """

    @staticmethod
    def create_vm(vm_id: int, name: str, status: str, host: str) -> VirtualMachine:
        """create and return a virtual machine
        """
        return VirtualMachine(vm_id, name, status, host)
