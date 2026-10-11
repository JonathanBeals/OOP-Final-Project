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


renderServers();