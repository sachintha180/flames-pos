export async function postJSON(routeURL, jsonObject) {
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
