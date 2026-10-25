"""abstract interface for virtual machine providers
"""

from abc import ABC, abstractmethod


class VMProvider(ABC):
    """define the interface for retrieving vm data
    """

    @abstractmethod
    def get_vm_data(self, vm_id: int) -> dict[str, object]:
        """get provider data for a vm
        """
