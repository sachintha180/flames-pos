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

function showError(errorMessage, errorAction, error=true) {
    const errorType = "FlamesPOS: Success";
    if (error) {
        errorType = "FlamesPOS: Error";
    }

    const errorTitle = document.querySelector("#error_title");
    const errorSubtitle = document.querySelector("#error_type");
    const errorLbl = document.querySelector("#error_lbl");

    const errorModal = document.querySelector("#error");

    errorTitle.innerHTML = errorMessage;
    errorSubtitle.innerHTML = errorType;
    errorLbl.innerHTML = errorAction;

    errorModal.setAttribute("open", true);
}

function hideError() {
    const errorTitle = document.querySelector("#error_title");
    const errorSubtitle = document.querySelector("#error_type");
    const errorLbl = document.querySelector("#error_lbl");

    const errorModal = document.querySelector("#error");

    errorTitle.innerHTML = "";
    errorSubtitle.innerHTML = "";
    errorLbl.innerHTML = "";

    errorModal.removeAttribute("open");
}
