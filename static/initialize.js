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
        const result = await response;
        return result;
    } catch (error) {
        return error;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.querySelector("#submit");
    const errorLbl = document.querySelector("#error p");

    submitBtn.addEventListener("click", () => {
        const username = document.querySelector("#username").value;
        const password = document.querySelector("#password").value;

        if (username && password) {
            authenticate(username, password).then((response) => {
                console.log(response);
            });
        } else {
            if (!username) {
                errorLbl.innerHTML = "Please enter a valid username";
            } else {
                errorLbl.innerHTML = "Please enter a valid password";
            }
        }
    });
});
