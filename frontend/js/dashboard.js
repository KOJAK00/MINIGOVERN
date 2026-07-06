console.log("dashboard.js loaded");
async function init() {

    const user = await checkAuth();

    if (!user) return;

    console.log(user);
}

init();

async function logout() {

    const token = localStorage.getItem("token");
    const response = await fetch(API + "/api/v1/user/logout", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    localStorage.removeItem("token");
    window.location.href = "index.html";

}