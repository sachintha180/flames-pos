function handleOwner() {
    hideError();
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
    const fullname = document.querySelector("#fullname").value;
    const mobile_no = document.querySelector("#mobile_no").value;

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
}

function resetDB(username, password) {
    hideError();

    let confirm = window.confirm(
        "Are you sure you want to reset the database?"
    );

    if (confirm) {
        postJSON("/reset_db", {
            username: username,
            password: password,
        }).then((response) => {
            showError(response.message, response.action, response.data.flag);
        });
    }
}

function handleAuth() {
    hideError();

    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    if (username && password) {
        postJSON("/initialize", {
            username: username,
            password: password,
        }).then((response) => {
            showError(response.message, response.action, response.data.flag);
            if (response.data.flag) {
                showMgmForm(response.data.owner_default);
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
}

function showMgmForm(owner_default) {
    const mgmContainer = document.querySelector("#manage");
    mgmContainer.innerHTML = `
        <h2>Manage FlamesPOS</h2>
        <form id="confirm_form">
            <label for="username">Username</label>  
            <input type="text" id="username" name="username" value="${owner_default.username}" required />
            <label for="password">Password</label>
            <input type="password" id="password" name="password" value='${owner_default.password}' required />
            <label for="password">Full Name</label>
            <input type="text" id="fullname" name="fullname" value='${owner_default.fullname}'required />
            <label for="password">Mobile No</label>
            <input type="text" id="mobile_no" name="mobile_no" value='${owner_default.mobile_no}' required />
            <section id="form_btns" class="grid">
                <input type="button" id="add_owner" name="add_owner" value="Add New Owner" />
                <input type="button" id="reset_db" name="reset_db" value="Reset Database" />
            </section>
        </form>
    `;
}

document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.querySelector("#submit");
    submitBtn.addEventListener("click", handleAuth);

    const errorCloseBtn = document.querySelector("#error_close");
    errorCloseBtn.addEventListener("click", hideError);
});
