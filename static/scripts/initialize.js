function handleOwner() {
    hideError();
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
    const fullname = document.querySelector("#fullname").value;
    const mobile_no = document.querySelector("#mobile_no").value;

    const addOwnerBtn = document.querySelector("#add_owner");
    setBtnBusy(addOwnerBtn, true);

    if (username && password && fullname && mobile_no) {
        postJSON("/add_owner", {
            username: username,
            password: password,
            fullname: fullname,
            mobile_no: mobile_no,
        }).then((response) => {
            showError(response.message, response.action, response.data.flag);
        });
    } else {
        if (!username) {
            showError("Invalid username", "Please enter a valid username");
        } else if (!password) {
            showError("Invalid password", "Please enter a valid password");
        } else if (!fullname) {
            showError("Invalid fullname", "Please enter a valid fullname");
        } else {
            showError("Invalid mobile no", "Please enter a valid mobile no");
        }
    }

    setBtnBusy(addOwnerBtn, false);
}

function resetDB(username, password) {
    hideError();

    const resetDBBtn = document.querySelector("#reset_db");
    setBtnBusy(resetDBBtn, true);

    let confirm = window.confirm(
        "Are you sure you want to reset the database? This action cannot be undone."
    );
    
    if (confirm) {
        postJSON("/reset_db", {
            username: username,
            password: password,
        }).then((response) => {
            showError(response.message, response.action, response.data.flag);
        });
    }

    setBtnBusy(resetDBBtn, false);
}

function handleAuth() {
    hideError();
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    const submitBtn = document.querySelector("#submit");
    setBtnBusy(submitBtn, true);

    if (username && password) {
        postJSON("/initialize", {
            username: username,
            password: password,
        }).then((response) => {
            showError(response.message, response.action, response.data.flag);
            if (response.data.flag) {
                document.querySelector("#manage").innerHTML = response.data.html;
                document
                    .querySelector("#add_owner")
                    .addEventListener("click", handleOwner);
                document
                    .querySelector("#reset_db")
                    .addEventListener("click", () => {
                        resetDB(username, password);
                    });
            }
        });
    } else {
        if (!username) {
            showError("Invalid username", "Please enter a valid username");
        } else {
            showError("Invalid password", "Please enter a valid password");
        }
    }

    setBtnBusy(submitBtn, false);
}

document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.querySelector("#submit");
    submitBtn.addEventListener("click", handleAuth);

    const errorCloseBtn = document.querySelector("#error_close");
    errorCloseBtn.addEventListener("click", hideError);
});
