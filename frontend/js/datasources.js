async function init() {

    const user = await checkAuth();

    if (!user) return;

    loadDatasources();

}

init();
async function scan(id) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        API + "/api/v1/scan/" + id,
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (response.ok) {
        alert("Scan started successfully and scan ID is: " + (await response.json()).id);
    } else {
        const data = await response.json();
        alert("Error: " + data.message);
    }
}
async function createDatasource() {
    const name =
        document.getElementById("name").value;
    const database_name =
        document.getElementById("database").value;
    const host =
        document.getElementById("host").value;
    const port =
        document.getElementById("port").value;
    const password =
        document.getElementById("password").value;
        const username =
        document.getElementById("username").value;

    const token = localStorage.getItem("token");
    
    const response = await fetch(
        API + "/api/v1/datasource/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                name,
                host,
                port,
                database_name,
                username,
                password,
                category_id: 1
            })
        }
    );
}
async function deleteDatasource(id) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        API + "/api/v1/datasource/" + id,
        {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (response.ok) {
        alert("Data source deleted successfully");
        loadDatasources();
    } else {
        const data = await response.json();
        console.log(data);
        alert("Error: " + data.detail);
    }
}

async function loadDatasources() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        API + "/api/v1/datasource/",
        {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const datasources = await response.json();
    const table =
        document.getElementById("datasource-table");
        table.innerHTML = "";
    datasources.forEach(ds => {
        table.innerHTML += `
        <tr>
            <td>${ds.name}</td>
            <td>${ds.database_name}</td>
            <td>${ds.host}</td>
            <td>${ds.port}</td>
            <td>
                <button
                    class="btn btn-success btn-sm"
                    onclick="scan(${ds.id})">
                    Scan
                </button>
                <button
                    class="btn btn-danger btn-sm"
                    onclick="deleteDatasource(${ds.id})">
                    Delete
                </button>
            </td>
        </tr>
        `;
    });

}