"""Tests for the Flask backend API."""

import pytest
from flask.testing import FlaskClient

from app.api import app, manager


@pytest.fixture(autouse=True)
def reset_manager() -> None:
    """Reset all VMManager state before each test."""
    manager.servers.clear()
    manager.clear_all_environments()


@pytest.fixture
def client() -> FlaskClient:
    """Create a Flask test client."""
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_get_servers(client: FlaskClient) -> None:
    """Test retrieving the default session servers."""
    response = client.get("/api/servers")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["server_id"] == 1
    assert data[0]["name"] == "Server1"
    assert data[1]["server_id"] == 2
    assert data[1]["name"] == "Server2"


def test_get_virtual_machines(client: FlaskClient) -> None:
    """Test retrieving the default session virtual machines."""
    response = client.get("/api/vms")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 4

    vm_ids = {vm["vm_id"] for vm in data}

    assert vm_ids == {1, 2, 3, 4}


def test_start_vm(client: FlaskClient) -> None:
    """Test starting a virtual machine."""
    response = client.post("/api/vms/2/start")

    assert response.status_code == 200

    data = response.get_json()

    assert data["vm_id"] == 2
    assert data["status"] == "running"


def test_stop_vm(client: FlaskClient) -> None:
    """Test stopping a virtual machine."""
    response = client.post("/api/vms/1/stop")

    assert response.status_code == 200

    data = response.get_json()

    assert data["vm_id"] == 1
    assert data["status"] == "stopped"


def test_restart_vm(client: FlaskClient) -> None:
    """Test restarting a virtual machine."""
    response = client.post("/api/vms/1/restart")

    assert response.status_code == 200

    data = response.get_json()

    assert data["vm_id"] == 1
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


def test_sessions_have_independent_vm_state() -> None:
    """Test that separate browser sessions have isolated VM state."""
    app.config["TESTING"] = True

    client_one = app.test_client()
    client_two = app.test_client()

    response_one = client_one.post("/api/vms/2/start")

    assert response_one.status_code == 200

    client_one_vms = client_one.get("/api/vms").get_json()
    client_two_vms = client_two.get("/api/vms").get_json()

    vm_two_client_one = next(
        vm for vm in client_one_vms
        if vm["vm_id"] == 2
    )

    vm_two_client_two = next(
        vm for vm in client_two_vms
        if vm["vm_id"] == 2
    )

    assert vm_two_client_one["status"] == "running"
    assert vm_two_client_two["status"] == "stopped"
