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

function handleAdmin() {
    const errorTitle = document.querySelector("#error_title");
    const errorLbl = document.querySelector("#error_lbl");
    errorTitle.innerHTML = "";
    errorLbl.innerHTML = "";

    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
    const fullname = document.querySelector("#fullname").value;
    const mobile_no = document.querySelector("#mobile_no").value;

    if (username && password && fullname && mobile_no) {
        postJSON("/add_admin", {
            username: username,
            password: password,
            fullname: fullname,
            mobile_no: mobile_no,
        }).then((response) => {
            errorTitle.innerHTML = response.message;
            errorLbl.innerHTML = response.action;
        });
    } else {
        if (!username) {
            errorTitle.innerHTML = "Invalid username";
            errorLbl.innerHTML = "Please enter a valid username";
        } else if (!password) {
            errorTitle.innerHTML = "Invalid password";
            errorLbl.innerHTML = "Please enter a valid password";
        } else if (!fullname) {
            errorTitle.innerHTML = "Invalid fullname";
            errorLbl.innerHTML = "Please enter a valid fullname";
        } else {
            errorTitle.innerHTML = "Invalid mobile no";
            errorLbl.innerHTML = "Please enter a valid mobile no";
        }
    }
}

function resetDB(username, password) {
    const errorTitle = document.querySelector("#error_title");
    const errorLbl = document.querySelector("#error_lbl");
    errorTitle.innerHTML = "";
    errorLbl.innerHTML = "";

    let confirm = window.confirm(
        "Are you sure you want to reset the database?"
    );

    if (confirm) {
        postJSON("/reset_db", {
            username: username,
            password: password,
        }).then((response) => {
            errorTitle.innerHTML = response.message;
            errorLbl.innerHTML = response.action;
        });
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
        postJSON("/initialize", {
            username: username,
            password: password,
        }).then((response) => {
            errorTitle.innerHTML = response.message;
            errorLbl.innerHTML = response.action;
            if (response.data.flag) {
                showConfirmForm(username, response.data.admin_default);
                document
                    .querySelector("#add_admin")
                    .addEventListener("click", handleAdmin);
                document
                    .querySelector("#reset_db")
                    .addEventListener("click", () => {
                        resetDB(username, password);
                    });
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

function showConfirmForm(username, admin_default) {
    const adminContainer = document.querySelector("#admin");
    adminContainer.innerHTML = `
        <h2>Welcome ${username}</h2>
        <h3>Admin Details</h3>
        <form id="confirm_form">
            <label for="username">Username</label>  
            <input type="text" id="username" name="username" value="${admin_default.username}" required />
            <label for="password">Password</label>
            <input type="password" id="password" name="password" value='${admin_default.password}' required />
            <label for="password">Full Name</label>
            <input type="text" id="fullname" name="fullname" value='${admin_default.name}'required />
            <label for="password">Mobile No</label>
            <input type="text" id="mobile_no" name="mobile_no" value='${admin_default.mobile_no}' required />
            <input type="button" id="add_admin" name="add_admin" value="Add New Admin" />
            <input type="button" id="reset_db" name="reset_db" value="Reset Database" />
        </form>
    `;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#submit").addEventListener("click", handleAuth);
});
