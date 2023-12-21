async function authenticate(username, password) {
    try {
        const response = await fetch("/initialize", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });
        const result = await response.json();
        return result;
    } catch (error) {
        return error;
    }
}

async function addAdmin(username, password, fullname, mobile_no) {
    try {
        const response = await fetch("/add_admin", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
                fullname: fullname,
                mobile_no: mobile_no,
            }),
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
        authenticate(username, password).then((response) => {
            errorTitle.innerHTML = response.message;
            errorLbl.innerHTML = response.action;
            if (response.data.flag) {
                showConfirmForm(username, response.data.admin_default);
                document
                    .querySelector("#add_admin")
                    .addEventListener("click", handleAdmin);
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
        addAdmin(username, password, fullname, mobile_no).then((response) => {
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
            <input type="button" id="clear_db" name="clear_db" value="Clear Database" />
        </form>
    `;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#submit").addEventListener("click", handleAuth);
});
