const servers = [
  {
    id: 1,
    name: "Server-01",
    status: "online"
  },
  {
    id: 2,
    name: "Server-02",
    status: "online"
  }
];

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
        <span>${server.id}</span>
      </div>
    `;

    serverList.appendChild(card);
  });
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

    // Create the container for VM controls.
    const controls = document.createElement("div");
    controls.className = "button-row";

    // Create the Start button.
    const startButton = document.createElement("button");
    startButton.textContent = "Start";
    startButton.className = "primary";
    startButton.disabled = vm.status === "running";

    // Create the Stop button.
    const stopButton = document.createElement("button");
    stopButton.textContent = "Stop";
    stopButton.className = "danger";
    stopButton.disabled = vm.status === "stopped";

    // Create the Restart button.
    const restartButton = document.createElement("button");
    restartButton.textContent = "Restart";
    restartButton.className = "ghost";
    restartButton.disabled = vm.status !== "running";

    // Add buttons to the controls container.
    controls.appendChild(startButton);
    controls.appendChild(stopButton);
    controls.appendChild(restartButton);

    // Add controls to the VM card.
    card.appendChild(controls);

    startButton.addEventListener("click", () => {
    vm.status = "running";
    renderVirtualMachines();
    });

    stopButton.addEventListener("click", () => {
    vm.status = "stopped";
    renderVirtualMachines();
    });

    restartButton.addEventListener("click", () => {
    vm.status = "running";
    renderVirtualMachines();
    });

    vmList.appendChild(card);
    });
    updateStatistics();
}

function refreshDashboard() {
    renderServers();
    renderVirtualMachines();

    const lastUpdated = document.getElementById("last-updated");
    lastUpdated.textContent = new Date().toLocaleTimeString();
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

const virtualMachines = [
  {
    id: 1,
    name: "Ubuntu-Web",
    status: "running",
    host: "Server-01"
  },
  {
    id: 2,
    name: "Kali-Linux",
    status: "stopped",
    host: "Server-01"
  },
  {
    id: 3,
    name: "Windows-11",
    status: "running",
    host: "Server-02"
  },
  {
    id: 4,
    name: "Debian-Test",
    status: "stopped",
    host: "Server-02"
  }
];

const refreshButton = document.getElementById("refresh");

refreshButton.addEventListener("click", refreshDashboard);

refreshDashboard();