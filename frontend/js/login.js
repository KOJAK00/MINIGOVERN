async function login() {
    const username =
        document.getElementById("username").value;
    const password =
        document.getElementById("password").value;
    const response = await fetch(
        API + "/api/v1/user/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        }
    );
    const data = await response.json();
    if (response.ok) {
        localStorage.setItem(
            "token",
            data.access_token
        );

        window.location.href =
            "dashboard.html";

    }
    else {
        document.getElementById("error_code").innerText =
            data.message;

    }

}