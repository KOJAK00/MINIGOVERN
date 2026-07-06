async function init() {

    const user = await checkAuth();

    if (!user) return;


}

async function loadSamples() {

    const datasetId = document.getElementById("dataset_id").value;

    if (!datasetId) {
        alert("Enter dataset id");
        return;
    }

    const token = localStorage.getItem("token");

    const response = await fetch(
        API + `/api/v1/masking/preview/${datasetId}`,
        {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        const data = await response.json();
        alert("Error: " + data.detail);
        return;
    }

    const rows = await response.json();

    const table = document.getElementById("sample-table");

    if (!table) {
        console.error("sample-table element not found in HTML");
        return;
    }

    if (!rows || rows.length === 0) {
        table.innerHTML = "<tr><td colspan='100%'>No data</td></tr>";
        return;
    }

    // headers (dynamic)
    const headers = Object.keys(rows[0]);

    let html = "";

    // table header
    html += "<tr>";
    headers.forEach(h => {
        html += `<th>${h}</th>`;
    });
    html += "</tr>";

    // table rows
    rows.forEach(row => {
        html += "<tr>";
        headers.forEach(h => {
            html += `<td>${row[h] ?? ""}</td>`;
        });
        html += "</tr>";
    });

    table.innerHTML = html;
}