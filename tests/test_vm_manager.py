"""Unit tests for the VMManager class."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.server import Server
from app.vm_manager import VMManager


@pytest.fixture(autouse=True)
def reset_manager() -> None:
    """Reset the Singleton between tests."""
    VMManager._instance = None


def test_singleton() -> None:
    """Test that VMManager only creates one instance."""
    manager_one = VMManager()
    manager_two = VMManager()

    assert manager_one is manager_two


def test_add_server() -> None:
    """Test adding a server to the manager."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)

    assert len(manager.servers) == 1
    assert manager.servers[0] is server


def test_get_server() -> None:
    """Test finding a server by ID."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)

    assert manager.get_server(1) is server


def test_get_nonexistent_server() -> None:
    """Test searching for a server that does not exist."""
    manager = VMManager()

    assert manager.get_server(99) is None


def test_create_vm() -> None:
    """Test creating a VM through the manager."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)

    vm = manager.create_vm(
        1,
        100,
        "Ubuntu",
        "stopped",
        "Server1"
    )

    assert vm is not None
    assert vm.vm_id == 100
    assert vm.name == "Ubuntu"
    assert vm.status == "stopped"
    assert vm.host == "Server1"
    assert vm in server.virtual_machines


def test_create_vm_invalid_server() -> None:
    """Test creating a VM on a server that does not exist."""
    manager = VMManager()

    vm = manager.create_vm(
        99,
        100,
        "Ubuntu",
        "stopped",
        "Server1"
    )

    assert vm is None


def test_start_vm() -> None:
    """Test starting a virtual machine."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)
    vm = manager.create_vm(1, 100, "Ubuntu", "stopped", "Server1")

    result = manager.start_vm(100)

    assert result is True
    assert vm is not None
    assert vm.status == "running"


def test_stop_vm() -> None:
    """Test stopping a virtual machine."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)
    vm = manager.create_vm(1, 100, "Ubuntu", "running", "Server1")

    result = manager.stop_vm(100)

    assert result is True
    assert vm is not None
    assert vm.status == "stopped"


def test_delete_vm() -> None:
    """Test deleting a virtual machine."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)
    manager.create_vm(1, 100, "Ubuntu", "stopped", "Server1")

    result = manager.delete_vm(100)

    assert result is True
    assert manager.get_virtual_machine(100) is None
    assert len(server.virtual_machines) == 0


def test_invalid_vm_operations() -> None:
    """Test operations on a VM that does not exist."""
    manager = VMManager()

    assert manager.start_vm(999) is False
    assert manager.stop_vm(999) is False
    assert manager.delete_vm(999) is False


@given(
    vm_id=st.integers(min_value=1, max_value=100000),
    name=st.text(min_size=1, max_size=30),
    host=st.text(min_size=1, max_size=30),
)
def test_create_vm_with_generated_values(
    vm_id: int,
    name: str,
    host: str
) -> None:
    """Test VM creation with generated values."""
    manager = VMManager()
    server = Server(1, "Server1", "online", "192.168.1.10")

    manager.add_server(server)

    vm = manager.create_vm(
        1,
        vm_id,
        name,
        "stopped",
        host
    )

    assert vm is not None
    assert vm.vm_id == vm_id
    assert vm.name == name
    assert vm.host == host
