"""unit testing for the VM adapter design pattern
"""

from unittest.mock import Mock
import pytest
from hypothesis import given, strategies as st
from app.simulated_provider import SimulatedProvider
from app.vm_adapter import VMAdapter
from app.virtual_machine import VirtualMachine


def test_adapter_creates_vm() -> None:
    """tests that the adapter creates a vm object
    """
    provider = SimulatedProvider()
    adapter = VMAdapter(provider)

    vm = adapter.get_virtual_machine(101)

    assert isinstance(vm, VirtualMachine)
    assert vm.vm_id == 101
    assert vm.name == "VM-101"
    assert vm.status == "stopped"
    assert vm.host == "server-1"


def test_adapter_running_vm() -> None:
    """Test that poweredOn is translated to running."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": 102,
        "vm_name": "Ubuntu",
        "power_state": "poweredOn",
        "node": "server-1"
    }

    adapter = VMAdapter(provider)
    vm = adapter.get_virtual_machine(102)

    assert vm.vm_id == 102
    assert vm.name == "Ubuntu"
    assert vm.status == "running"
    assert vm.host == "server-1"

    provider.get_vm_data.assert_called_once_with(102)


def test_adapter_suspended_vm() -> None:
    """Test that suspended is translated to paused."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": 103,
        "vm_name": "Windows",
        "power_state": "suspended",
        "node": "server-2"
    }

    adapter = VMAdapter(provider)
    vm = adapter.get_virtual_machine(103)

    assert vm.vm_id == 103
    assert vm.name == "Windows"
    assert vm.status == "paused"
    assert vm.host == "server-2"


def test_adapter_invalid_power_state() -> None:
    """Test that an unknown power state raises ValueError."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": 104,
        "vm_name": "Ubuntu",
        "power_state": "broken",
        "node": "server-1"
    }

    adapter = VMAdapter(provider)

    with pytest.raises(ValueError, match="Unknown VM power state"):
        adapter.get_virtual_machine(104)


def test_adapter_missing_power_state() -> None:
    """Test that a missing power state raises ValueError."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": 105,
        "vm_name": "Ubuntu",
        "node": "server-1"
    }

    adapter = VMAdapter(provider)

    with pytest.raises(ValueError, match="Invalid or missing VM power state"):
        adapter.get_virtual_machine(105)


def test_adapter_missing_vm_name() -> None:
    """Test that a missing VM name raises ValueError."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": 106,
        "power_state": "poweredOn",
        "node": "server-1"
    }

    adapter = VMAdapter(provider)

    with pytest.raises(ValueError, match="Invalid or missing VM name"):
        adapter.get_virtual_machine(106)


def test_adapter_invalid_vm_id() -> None:
    """Test that an invalid VM ID raises ValueError."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": "invalid",
        "vm_name": "Ubuntu",
        "power_state": "poweredOn",
        "node": "server-1"
    }

    adapter = VMAdapter(provider)

    with pytest.raises(ValueError, match="Invalid or missing VM id"):
        adapter.get_virtual_machine(107)


def test_adapter_missing_host() -> None:
    """Test that a missing VM host raises ValueError."""
    provider = Mock(spec=SimulatedProvider)

    provider.get_vm_data.return_value = {
        "id": 108,
        "vm_name": "Ubuntu",
        "power_state": "poweredOn"
    }

    adapter = VMAdapter(provider)

    with pytest.raises(ValueError, match="Invalid or missing VM host"):
        adapter.get_virtual_machine(108)


def test_adapter_multiple_vms() -> None:
    """Test that the adapter creates independent VM objects."""
    provider = SimulatedProvider()
    adapter = VMAdapter(provider)

    vm1 = adapter.get_virtual_machine(201)
    vm2 = adapter.get_virtual_machine(202)

    assert vm1.vm_id == 201
    assert vm2.vm_id == 202
    assert vm1.name == "VM-201"
    assert vm2.name == "VM-202"
    assert vm1 is not vm2


@given(vm_id=st.integers(min_value=1, max_value=100000))
def test_adapter_hypothesis_vm_ids(vm_id: int) -> None:
    """Test VM creation using automatically generated IDs."""
    provider = SimulatedProvider()
    adapter = VMAdapter(provider)

    vm = adapter.get_virtual_machine(vm_id)

    assert isinstance(vm, VirtualMachine)
    assert vm.vm_id == vm_id
    assert vm.name == f"VM-{vm_id}"
    assert vm.status == "stopped"
    assert vm.host == "server-1"
