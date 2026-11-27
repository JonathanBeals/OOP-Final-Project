"""simulated vm provider
"""

from app.vm_provider import VMProvider


class SimulatedProvider(VMProvider):
    """provide simulated virtual machine data
    """

    def get_vm_data(self, vm_id: int) -> dict[str, object]:
        """_summary_
        """
        return {
            "id": vm_id,
            "vm_name": f"VM-{vm_id}",
            "power_state": "poweredOff",
            "node": "server-1"
        }
