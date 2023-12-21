async function postJSON(routeURL, jsonObject) {
    try {
        const response = await fetch(routeURL, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify(jsonObject),
        });
        const result = await response.json();
        return result;
    } catch (error) {
        return error;
    }
}


function handleAuth() {
    const errorTitle = document.querySelector("#error_title");
    const errorLbl = document.querySelector("#error_lbl");
    errorTitle.innerHTML = "";
    errorLbl.innerHTML = "";

    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    if (username && password) {
        postJSON("/login", {
            username: username,
            password: password,
        }).then((response) => {
            if (response.status_code != 200) {
                errorTitle.innerHTML = response.message;
                errorLbl.innerHTML = response.action;
            } else {
                console.log(response);
            }
        });
    } else {
        if (!username) {
            errorTitle.innerHTML = "Invalid username";
            errorLbl.innerHTML = "Please enter a valid username";
        } else {
            errorTitle.innerHTML = "Invalid password";
            errorLbl.innerHTML = "Please enter a valid password";
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#submit").addEventListener("click", handleAuth);
});
