"""Flask backend API for the VM management system."""

from flask import Flask, Response, jsonify

from app.server import Server
from app.vm_manager import VMManager

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

manager = VMManager()


@app.get("/")
def dashboard() -> Response:
    """Serve the web dashboard."""
    return app.send_static_file("index.html")


def initialize_demo_data() -> None:
    """Create sample servers and virtual machines."""
    if manager.servers:
        return

    server_one = Server(
        1,
        "Server1",
        "online",
        "192.168.1.10"
    )

    server_two = Server(
        2,
        "Server2",
        "online",
        "192.168.1.20"
    )

    manager.add_server(server_one)
    manager.add_server(server_two)

    manager.create_vm(
        1,
        1,
        "Ubuntu-Web",
        "running",
        "Server1"
    )

    manager.create_vm(
        1,
        2,
        "Kali-Linux",
        "stopped",
        "Server1"
    )

    manager.create_vm(
        2,
        3,
        "Windows-11",
        "running",
        "Server2"
    )

    manager.create_vm(
        2,
        4,
        "Debian-Test",
        "stopped",
        "Server2"
    )


@app.get("/api/servers")
def get_servers() -> tuple[Response, int]:
    """Return all servers as JSON."""
    servers = []

    for server in manager.servers:
        servers.append(
            {
                "server_id": server.server_id,
                "name": server.name,
                "status": server.status,
                "address": server.address,
                "virtual_machine_count": len(server.virtual_machines),
            }
        )

    return jsonify(servers), 200


@app.get("/api/vms")
def get_virtual_machines() -> tuple[Response, int]:
    """Return all virtual machines as JSON."""
    virtual_machines = []

    for server in manager.servers:
        for vm in server.virtual_machines:
            virtual_machines.append(
                {
                    "vm_id": vm.vm_id,
                    "name": vm.name,
                    "status": vm.status,
                    "host": vm.host,
                }
            )

    return jsonify(virtual_machines), 200


@app.post("/api/vms/<int:vm_id>/start")
def start_virtual_machine(vm_id: int) -> tuple[Response, int]:
    """Start a virtual machine."""
    if not manager.start_vm(vm_id):
        return jsonify({"error": "Virtual machine not found"}), 404

    return jsonify(
        {
            "message": "Virtual machine started",
            "vm_id": vm_id,
            "status": "running",
        }
    ), 200


@app.post("/api/vms/<int:vm_id>/stop")
def stop_virtual_machine(vm_id: int) -> tuple[Response, int]:
    """Stop a virtual machine."""
    if not manager.stop_vm(vm_id):
        return jsonify({"error": "Virtual machine not found"}), 404

    return jsonify(
        {
            "message": "Virtual machine stopped",
            "vm_id": vm_id,
            "status": "stopped",
        }
    ), 200


@app.post("/api/vms/<int:vm_id>/restart")
def restart_virtual_machine(vm_id: int) -> tuple[Response, int]:
    """Restart a virtual machine."""
    vm = manager.get_virtual_machine(vm_id)

    if vm is None:
        return jsonify({"error": "Virtual machine not found"}), 404

    vm.status = "stopped"
    vm.status = "running"

    return jsonify(
        {
            "message": "Virtual machine restarted",
            "vm_id": vm_id,
            "status": "running",
        }
    ), 200


initialize_demo_data()

manager.create_vm(
    1, 101, "Ubuntu-Web", "running", "Server1"
)
manager.create_vm(
    1, 102, "Database", "stopped", "Server1"
)
manager.create_vm(
    2, 103, "Kali-Linux", "running", "Server2"
)
manager.create_vm(
    2, 104, "Windows-Server", "stopped", "Server2"
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
