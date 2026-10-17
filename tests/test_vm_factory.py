"""tests for vm_factory.py
"""

from app.vm_factory import VmFactory


def test_vm_factory():
    """testing the arguments in the virtual machine
    """
    vm = VmFactory.create_vm(1, "Ubuntu", "stopped", "server 1")

    assert vm.vm_id == 1
    assert vm.name == "Ubuntu"
    assert vm.status == "stopped"
    assert vm.host == "server 1"


def test_create_multiple_vms():
    """testing the creation of multiple vms
    """
    vm1 = VmFactory.create_vm(1, "Ubuntu", "stopped", "server 1")
    vm2 = VmFactory.create_vm(2, "Kali Linux", "stopped", "server 1")

    assert vm1 is not vm2
    assert vm2.name == "Kali Linux"


def test_create_running_vm():
    """testing creation of a running virtual machine
    """
    vm = VmFactory.create_vm(10, "Windows 11", "running", "server 2")

    assert vm.status == "running"
    assert vm.host == "server 2"
