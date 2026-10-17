"""Unit tests for the VirtualMachine class."""

from app.virtual_machine import VirtualMachine


def test_virtual_machine_initialization():
    """Test that a VirtualMachine is initialized correctly."""
    vm = VirtualMachine(1, "Ubuntu", "stopped", "server1")

    assert vm.vm_id == 1
    assert vm.name == "Ubuntu"
    assert vm.status == "stopped"
    assert vm.host == "server1"


def test_name_setter():
    """Test changing the name of a virtual machine."""
    vm = VirtualMachine(1, "Ubuntu", "stopped", "server1")

    vm.name = "Ubuntu-Web"

    assert vm.name == "Ubuntu-Web"


def test_status_setter():
    """Test changing the status of a virtual machine."""
    vm = VirtualMachine(1, "Ubuntu", "stopped", "server1")

    vm.status = "running"

    assert vm.status == "running"


def test_host_setter():
    """Test changing the host of a virtual machine."""
    vm = VirtualMachine(1, "Ubuntu", "stopped", "server1")

    vm.host = "server2"

    assert vm.host == "server2"