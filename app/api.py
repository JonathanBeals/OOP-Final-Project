"""Flask backend API for the VM management system."""

from uuid import uuid4

from flask import Flask, Response, jsonify, session

from app.server import Server
from app.vm_manager import VMManager


app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

app.secret_key = "dev-secret-key"

manager = VMManager()


@app.get("/")
def dashboard() -> Response:
    """Serve the web dashboard."""
    return app.send_static_file("index.html")


def get_environment_id() -> str:
    """Return the current browser session environment ID."""
    if "environment_id" not in session:
        session["environment_id"] = str(uuid4())

    return str(session["environment_id"])


def initialize_demo_data(environment_id: str) -> None:
    """Create sample servers and virtual machines for one session."""
    servers = manager.get_environment_servers(environment_id)

    if servers:
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

    manager.add_server(
        server_one,
        environment_id
    )

    manager.add_server(
        server_two,
        environment_id
    )

    manager.create_vm(
        1,
        1,
        "Ubuntu-Web",
        "running",
        "Server1",
        environment_id
    )

    manager.create_vm(
        1,
        2,
        "Kali-Linux",
        "stopped",
        "Server1",
        environment_id
    )

    manager.create_vm(
        2,
        3,
        "Windows-11",
        "running",
        "Server2",
        environment_id
    )

    manager.create_vm(
        2,
        4,
        "Debian-Test",
        "stopped",
        "Server2",
        environment_id
    )


@app.get("/api/servers")
def get_servers() -> tuple[Response, int]:
    """Return all servers for the current session as JSON."""
    environment_id = get_environment_id()
    initialize_demo_data(environment_id)

    servers = []

    for server in manager.get_environment_servers(environment_id):
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
    """Return all virtual machines for the current session as JSON."""
    environment_id = get_environment_id()
    initialize_demo_data(environment_id)

    virtual_machines = []

    for server in manager.get_environment_servers(environment_id):
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
    """Start a virtual machine for the current session."""
    environment_id = get_environment_id()
    initialize_demo_data(environment_id)

    if not manager.start_vm(
        vm_id,
        environment_id
    ):
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
    """Stop a virtual machine for the current session."""
    environment_id = get_environment_id()
    initialize_demo_data(environment_id)

    if not manager.stop_vm(
        vm_id,
        environment_id
    ):
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
    """Restart a virtual machine for the current session."""
    environment_id = get_environment_id()
    initialize_demo_data(environment_id)

    vm = manager.get_virtual_machine(
        vm_id,
        environment_id
    )

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
