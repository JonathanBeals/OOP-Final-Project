"""Tests for the Flask backend API."""

import pytest
from flask.testing import FlaskClient

from app.api import app, manager
from app.server import Server


@pytest.fixture(autouse=True)
def reset_manager() -> None:
    """Reset VMManager data before every test."""
    manager.servers.clear()


@pytest.fixture
def client() -> FlaskClient:
    """Create a Flask test client."""
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def create_test_server() -> Server:
    """Create and register a server for API tests."""
    server = Server(
        1,
        "Server1",
        "online",
        "192.168.1.10"
    )

    manager.add_server(server)

    return server


def create_test_vm() -> None:
    """Create a virtual machine for API tests."""
    create_test_server()

    manager.create_vm(
        1,
        100,
        "Ubuntu",
        "stopped",
        "Server1"
    )


def test_get_servers(client: FlaskClient) -> None:
    """Test retrieving all servers."""
    create_test_server()

    response = client.get("/api/servers")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["server_id"] == 1
    assert data[0]["name"] == "Server1"
    assert data[0]["status"] == "online"


def test_get_virtual_machines(client: FlaskClient) -> None:
    """Test retrieving all virtual machines."""
    create_test_vm()

    response = client.get("/api/vms")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["vm_id"] == 100
    assert data[0]["name"] == "Ubuntu"
    assert data[0]["status"] == "stopped"


def test_start_vm(client: FlaskClient) -> None:
    """Test starting a virtual machine."""
    create_test_vm()

    response = client.post("/api/vms/100/start")

    assert response.status_code == 200

    data = response.get_json()

    assert data["vm_id"] == 100
    assert data["status"] == "running"


def test_stop_vm(client: FlaskClient) -> None:
    """Test stopping a virtual machine."""
    create_test_vm()

    manager.start_vm(100)

    response = client.post("/api/vms/100/stop")

    assert response.status_code == 200

    data = response.get_json()

    assert data["vm_id"] == 100
    assert data["status"] == "stopped"


def test_restart_vm(client: FlaskClient) -> None:
    """Test restarting a virtual machine."""
    create_test_vm()

    response = client.post("/api/vms/100/restart")

    assert response.status_code == 200

    data = response.get_json()

    assert data["vm_id"] == 100
    assert data["status"] == "running"


def test_start_missing_vm(client: FlaskClient) -> None:
    """Test starting a VM that does not exist."""
    response = client.post("/api/vms/999/start")

    assert response.status_code == 404


def test_stop_missing_vm(client: FlaskClient) -> None:
    """Test stopping a VM that does not exist."""
    response = client.post("/api/vms/999/stop")

    assert response.status_code == 404


def test_restart_missing_vm(client: FlaskClient) -> None:
    """Test restarting a VM that does not exist."""
    response = client.post("/api/vms/999/restart")

    assert response.status_code == 404
