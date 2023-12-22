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

function showError(errorMessage, errorAction) {
    const errorTitle = document.querySelector("#error_title");
    const errorLbl = document.querySelector("#error_lbl");
    const errorModal = document.querySelector("#error");

    errorTitle.innerHTML = errorMessage;
    errorLbl.innerHTML = errorAction;

    errorModal.setAttribute("open", true);
}

function hideError() {
    const errorTitle = document.querySelector("#error_title");
    const errorLbl = document.querySelector("#error_lbl");
    const errorModal = document.querySelector("#error");

    errorTitle.innerHTML = "";
    errorLbl.innerHTML = "";

    errorModal.removeAttribute("open");
}

function handleAuth() {
    hideError();
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    if (username && password) {
        postJSON("/login", {
            username: username,
            password: password,
        }).then((response) => {
            showError(response.message, response.action);
            if (response.data.flag) {
                window.location.href = "/menu";
            }
        });
    } else {
        if (!username) {
            showError("Invalid username", "Please enter a valid username");
        } else {
            showError("Invalid password", "Please enter a valid password");
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.querySelector("#submit");
    submitBtn.addEventListener("click", handleAuth);

    const errorCloseBtn = document.querySelector("#error_close");
    errorCloseBtn.addEventListener("click", hideError);
});
