let servers = [];
let virtualMachines = [];

function showError(message) {
  console.error(message);
  alert(message);
}

async function fetchServers() {
  const response = await fetch("/api/servers");

  if (!response.ok) {
    throw new Error("Failed to load servers");
  }

  servers = await response.json();
}

async function fetchVirtualMachines() {
  const response = await fetch("/api/vms");

  if (!response.ok) {
    throw new Error("Failed to load virtual machines");
  }

  virtualMachines = await response.json();
}

function renderServers() {
  const serverList = document.getElementById("server-list");
  serverList.innerHTML = "";

  servers.forEach((server) => {
    const card = document.createElement("div");
    card.className = "server-card";

    card.innerHTML = `
      <div class="server-top">
        <strong>${server.name}</strong>
        <span class="badge ${server.status}">
          ${server.status}
        </span>
      </div>

      <div class="meta-row">
        <span>Server ID</span>
        <span>${server.server_id}</span>
      </div>

      <div class="meta-row">
        <span>Address</span>
        <span>${server.address}</span>
      </div>
    `;

    serverList.appendChild(card);
  });
}

async function performVmAction(vmId, action) {
  const response = await fetch(
    `/api/vms/${vmId}/${action}`,
    {
      method: "POST"
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to ${action} virtual machine`);
  }

  await refreshDashboard();
}

function renderVirtualMachines() {
  const vmList = document.getElementById("vm-list");
  vmList.innerHTML = "";

  virtualMachines.forEach((vm) => {
    const card = document.createElement("div");
    card.className = "server-card";

    const top = document.createElement("div");
    top.className = "server-top";

    const name = document.createElement("strong");
    name.textContent = vm.name;

    const badge = document.createElement("span");
    badge.className = `badge ${vm.status}`;
    badge.textContent = vm.status;

    const host = document.createElement("div");
    host.className = "meta-row";
    host.textContent = `Host: ${vm.host}`;

    top.appendChild(name);
    top.appendChild(badge);

    card.appendChild(top);
    card.appendChild(host);

    const controls = document.createElement("div");
    controls.className = "button-row";

    const startButton = document.createElement("button");
    startButton.textContent = "Start";
    startButton.className = "primary";
    startButton.disabled = vm.status === "running";

    const stopButton = document.createElement("button");
    stopButton.textContent = "Stop";
    stopButton.className = "danger";
    stopButton.disabled = vm.status === "stopped";

    const restartButton = document.createElement("button");
    restartButton.textContent = "Restart";
    restartButton.className = "ghost";
    restartButton.disabled = vm.status !== "running";

    startButton.addEventListener("click", async () => {
      startButton.disabled = true;

      try {
        await performVmAction(vm.vm_id, "start");
      } catch (error) {
        showError(error.message);
      }
    });

    stopButton.addEventListener("click", async () => {
      stopButton.disabled = true;

      try {
        await performVmAction(vm.vm_id, "stop");
      } catch (error) {
        showError(error.message);
      }
    });

    restartButton.addEventListener("click", async () => {
      restartButton.disabled = true;

      try {
        await performVmAction(vm.vm_id, "restart");
      } catch (error) {
        showError(error.message);
      }
    });

    controls.appendChild(startButton);
    controls.appendChild(stopButton);
    controls.appendChild(restartButton);

    card.appendChild(controls);

    vmList.appendChild(card);
  });

  updateStatistics();
}

function updateStatistics() {
  const runningVMs = virtualMachines.filter(
    (vm) => vm.status === "running"
  ).length;

  const stoppedVMs = virtualMachines.filter(
    (vm) => vm.status === "stopped"
  ).length;

  document.getElementById("total-servers").textContent =
    servers.length;

  document.getElementById("running-vms").textContent =
    runningVMs;

  document.getElementById("stopped-vms").textContent =
    stoppedVMs;
}

async function refreshDashboard() {
  const refreshButton = document.getElementById("refresh");

  if (refreshButton) {
    refreshButton.disabled = true;
  }

  try {
    await Promise.all([
      fetchServers(),
      fetchVirtualMachines()
    ]);

    renderServers();
    renderVirtualMachines();

    const lastUpdated = document.getElementById("last-updated");

    if (lastUpdated) {
      lastUpdated.textContent =
        new Date().toLocaleTimeString();
    }
  } catch (error) {
    showError(error.message);
  } finally {
    if (refreshButton) {
      refreshButton.disabled = false;
    }
  }
}

const refreshButton = document.getElementById("refresh");

refreshButton.addEventListener(
  "click",
  refreshDashboard
);

refreshDashboard();