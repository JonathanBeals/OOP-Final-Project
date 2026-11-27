"""adapter for converting provider into VM objects
"""
from app.vm_provider import VMProvider
from app.virtual_machine import VirtualMachine
from app.vm_factory import VmFactory


class VMAdapter:
    """convert provider data into vm objects
    """

    def __init__(self, provider: VMProvider) -> None:
        """initialize the adapter

        Args:
            provider (VMProvider): provider supplying virtual machine data
        """
        self._provider = provider

    def get_virtual_machine(self, vm_id: int) -> VirtualMachine:
        """retrieve and adapt provider data into a VirtualMachin

        Args:
            vm_id (int): id of the vm

        Returns:
            VirtualMachine: the adapted vm object
        """
        raw_data = self._provider.get_vm_data(vm_id)
        power_state = raw_data.get("power_state")

        if not isinstance(power_state, str):
            raise ValueError("Invalid or missing VM power state")

        power_states = {
            "poweredOn": "running",
            "poweredOff": "stopped",
            "suspended": "paused"
        }
        status = power_states.get(power_state)

        if status is None:
            raise ValueError(f"Unknown VM power state: {power_state}")

        vm_id_data = raw_data.get("id")
        name = raw_data.get("vm_name")
        host = raw_data.get("node")

        if not isinstance(vm_id_data, int):
            raise ValueError("Invalid or missing VM id")
        if not isinstance(name, str):
            raise ValueError("Invalid or missing VM name")
        if not isinstance(host, str):
            raise ValueError("Invalid or missing VM host")

        return VmFactory.create_vm(
            vm_id_data,
            name,
            status,
            host
        )
