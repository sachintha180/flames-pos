function handleAuth() {
    hideError();
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    if (username && password) {
        postJSON("/login", {
            username: username,
            password: password,
        }).then((response) => {
            showError(response.message, response.action, response.data.flag);
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
