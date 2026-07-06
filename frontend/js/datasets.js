async function init() {

    const user = await checkAuth();

    if (!user) return;

    loadDatasets();

}

init();
async function submitDataset(id) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        API + "/api/v1/dataset/" + id + "/submit",
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (response.ok) {
        alert("Dataset submitted successfully");
        loadDatasets();
    } else {
        const data = await response.json();
        alert("Error: " + data.detail);
    }
}
async function approveDataset(id) {

    const token = localStorage.getItem("token");

    const response = await fetch(
        API + "/api/v1/dataset/" + id + "/approve",
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (response.ok) {
        alert("Dataset approved successfully");
        loadDatasets();
    } else {
        const data = await response.json();
        alert("Error: " + data.detail);
    }
}
async function rejectDataset(id) {

    const token = localStorage.getItem("token");


    const response = await fetch(
        API + "/api/v1/dataset/" + id + "/reject",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                comment: "Rejected by admin"
            })
        }
    );

    if (response.ok) {
        alert("Dataset rejected successfully");
        loadDatasets();
    } else {
        const data = await response.json();
        alert("Error: " + data.detail);
    }
}

async function loadDatasets() {

    const token = localStorage.getItem("token");
    const response = await fetch(
        API + "/api/v1/dataset/",
        {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const datasources = await response.json();
    const table =
        document.getElementById("dataset-table");
        table.innerHTML = "";
    datasources.forEach(ds => {
        table.innerHTML += `
        <tr>
            <td>${ds.id}</td>
            <td>${ds.name}</td>
            <td>${ds.datasource_id}</td>
            <td>${ds.scan_job_id}</td>
            <td>${ds.state}</td>
            <td>${ds.rejection_comment}</td>
        <td>
                <button
                    class="btn btn-success btn-sm"
                    onclick="submitDataset(${ds.id})">
                    Submit
                </button>
                <button
                    class="btn btn-success btn-sm"
                    onclick="approveDataset(${ds.id})">
                    Approve
                </button>
                <button
                    class="btn btn-danger btn-sm"
                    onclick="rejectDataset(${ds.id})">
                    Reject
                </button>
            </td>
        </tr>
        `;
    });

}
  