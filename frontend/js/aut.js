async function checkAuth() {

    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "index.html";
        return null;
    }

    const response = await fetch(API + "/api/v1/user/me", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (!response.ok) {
        localStorage.removeItem("token");
        window.location.href = "index.html";
        return null;
    }

    return await response.json();
}