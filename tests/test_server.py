"""unit testing for server class
"""

from app.server import Server
from app.virtual_machine import VirtualMachine


def test_server_init() -> None:
    """"test if server initialized correct"""
    server = Server(1, "server 1", "online", "192.168.1.1")

    assert server.server_id == 1
    assert server.name == "server 1"
    assert server.status == "online"
    assert server.address == "192.168.1.1"
    assert server.virtual_machines == []


def test_empty_name() -> None:
    """test if server has an empty name
    """
    server = Server(2, "", "offline", "192.168.1.2")

    assert server.server_id == 2
    assert server.name == ""
    assert server.status == "offline"
    assert server.address == "192.168.1.2"
    assert server.virtual_machines == []


def test_diff_values() -> None:
    """test if server has different values
    """
    server = Server(3, "server 3", "in repair", "192.168.1.3")

    assert server.server_id == 3
    assert server.name == "server 3"
    assert server.status == "in repair"
    assert server.address == "192.168.1.3"
    assert server.virtual_machines == []


def test_name() -> None:
    """testing server name mismatch
    """
    server = Server(1, "server 1", "online", "192.168.1.1")

    server.name = "server 2"

    assert server.name == "server 2"


def test_name_empty() -> None:
    """testing empty server name
    """
    server = Server(1, "server1", "online", "192.168.1.1")

    server.name = ""

    assert server.name == ""


def test_name_twice() -> None:
    """testing changing the name twice
    """
    server = Server(3, "server 3", "online", "192.168.1.3")

    server.name = "server 4"
    server.name = "server 5"

    assert server.name == "server 5"


def test_status_change() -> None:
    """testing changing the status of the server
        """
    server = Server(1, "server 1", "online", "192.168.1.1")

    server.status = "offline"

    assert server.status == "offline"


def test_status_maint() -> None:
    """testing changing the status to maintenence
        """
    server = Server(2, "server 2", "online", "192.168.1.2")

    server.status = "maintenence"

    assert server.status == "maintenence"


def test_status_twice() -> None:
    """testing changing the name twice
    """
    server = Server(3, "server 3", "offline", "192.168.1.3")

    server.status = "online"
    server.status = "repair"

    assert server.status == "repair"


def test_address_change() -> None:
    """testing changing the ip address of the server
        """
    server = Server(1, "server 1", "online", "192.168.1.1")

    server.address = "192.168.1.2"

    assert server.address == "192.168.1.2"


def test_address_empty() -> None:
    """testing changing the ip address of the server to an empty address
        """
    server = Server(1, "server 1", "online", "192.168.1.2")

    server.address = ""

    assert server.address == ""


def test_address_twice() -> None:
    """testing changing the ip address of the server twice
        """
    server = Server(1, "server 1", "online", "192.168.1.1")

    server.address = "192.168.1.2"
    server.address = "192.168.1.3"

    assert server.address == "192.168.1.3"


def test_add_vm() -> None:
    """testing adding 1 virtual machine
    """
    server = Server(1, "server 2", "online", "192.168.1.1")
    vm = VirtualMachine(1, "Ubuntu", "stopped", "server 1")

    server.add_virtual_machine(vm)

    assert len(server.virtual_machines) == 1
    assert server.virtual_machines[0] == vm


def test_add_three_vms() -> None:
    """testing adding 3 virtual machines
    """
    server = Server(1, "server 1", "online", "192.168.1.1")

    vm1 = VirtualMachine(1, "Ubuntu", "stopped", "server 1")
    vm2 = VirtualMachine(2, "Kali Linux", "stopped", "server 1")
    vm3 = VirtualMachine(3, "Debian", "stopped", "server 1")

    server.add_virtual_machine(vm1)
    server.add_virtual_machine(vm2)
    server.add_virtual_machine(vm3)

    assert len(server.virtual_machines) == 3
    assert server.virtual_machines[0] == vm1
    assert server.virtual_machines[1] == vm2
    assert server.virtual_machines[2] == vm3


def test_add_vm_twice() -> None:
    """trying to add the same vm twice
    """
    server = Server(1, "server 1", "online", "192.168.1.1")

    vm = VirtualMachine(1, "Kali Linux", "stopped", "server 1")

    server.add_virtual_machine(vm)
    server.add_virtual_machine(vm)

    assert server.virtual_machines[0] == vm
    assert server.virtual_machines[1] == vm


def test_remove_vm() -> None:
    """testing the removal of one vm
    """
    server = Server(1, "server 1", "online", "192.168.1.1")

    vm1 = VirtualMachine(1, "Ubuntu", "running", "server 1")
    vm2 = VirtualMachine(2, "Kali", "running", "server 1")

    server.add_virtual_machine(vm1)
    server.add_virtual_machine(vm2)

    server.remove_virtual_machine(1)

    assert len(server.virtual_machines) == 1
    assert server.virtual_machines[0] == vm2


def test_remove_nonexistent_vm() -> None:
    """testing removing a vm that doesnt exist
    """
    server = Server(1, "server 1", "online", "192.168.1.1")

    vm = VirtualMachine(1, "Kali Linux", "online", "server 1")
    server.add_virtual_machine(vm)

    server.remove_virtual_machine(100)

    assert len(server.virtual_machines) == 1
    assert server.virtual_machines[0] == vm


def test_remove_three_vms() -> None:
    """testing the removal of three vms
    """
    server = Server(1, "server 1", "online", "192.168.1.1")

    vm1 = VirtualMachine(1, "Ubuntu", "running", "server 1")
    vm2 = VirtualMachine(2, "Kali", "running", "server 1")
    vm3 = VirtualMachine(3, "Debian", "running", "server 1")

    server.add_virtual_machine(vm1)
    server.add_virtual_machine(vm2)
    server.add_virtual_machine(vm3)

    server.remove_virtual_machine(1)
    server.remove_virtual_machine(2)
    server.remove_virtual_machine(3)

    assert len(server.virtual_machines) == 0
    assert server.virtual_machines == []
