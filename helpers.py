"""
helpers.py (docstring generated by DuetAI).

This module contains helper functions for the Flames POS application.
The helper functions are:
- generate_response: Generates a JSON response with a status code, message, action, and data.
- check_credential_presence: Checks if the request JSON contains the username and password and is not empty.
- verify_credentials: Verifies the provided credentials against the actual credentials.
"""

from flask import jsonify


def generate_response(status_code, message, action, data):
    """Generate a JSON response with a status code, message, action, and data.

    Args:
        status_code (int): the status code of the response
        message (str): the message of the response
        action (str): the action of the response
        data (dict): the data of the response
    Returns:
        response (Response): the JSON response with a status code, message, action, and data
    """

    response = jsonify({"message": message, "action": action, "data": data})
    response.status_code = status_code
    return response


def check_credential_presence(request_json):
    """Check if the request JSON contains the username and password and is not empty.

    Args:
        request_json (dict): the request JSON
    Returns:
        if valid:
            (tuple, bool): (username, password), valid=True
        else:
            (Response, bool): Response with a status code, message, action, and data, valid=False
    """

    valid = False

    try:
        username = request_json["username"]
    except KeyError:
        return (
            generate_response(
                status_code=400,
                message="Username not received",
                action="Please refresh your page and try logging in again",
                data={"authenticated": False},
            ),
            valid,
        )

    try:
        password = request_json["password"]
    except KeyError:
        return (
            generate_response(
                status_code=400,
                message="Password not received",
                action="Please refresh your page and try logging in again",
                data={"authenticated": False},
            ),
            valid,
        )

    if username is None:
        return (
            generate_response(
                status_code=400,
                message="Empty username",
                action="Please enter a valid username",
                data={"authenticated": False},
            ),
            valid,
        )

    if password is None:
        return (
            generate_response(
                status_code=400,
                message="Empty password",
                action="Please enter a valid password",
                data={"authenticated": False},
            ),
            valid,
        )

    valid = True

    return (username, password), valid


def verify_credentials(provided_creds, actual_creds):
    """Verify the provided credentials against the actual credentials.

    Args:
        provided_creds (dict): the provided credentials; username and password
        actual_creds (dict): the actual credentials; username and password
    Returns:
        response (Response): Response with a status code, message, action, and data
    """

    if provided_creds["username"] != actual_creds["username"]:
        return generate_response(
            status_code=401,
            message="Invalid username",
            action="Please enter the correct username",
            data={"authenticated": False},
        )

    elif provided_creds["password"] != actual_creds["password"]:
        return generate_response(
            status_code=401,
            message="Invalid password",
            action="Please enter the correct password",
            data={"authenticated": False},
        )

    return generate_response(
        status_code=200,
        message="Login successful",
        action="You are now logged in",
        data={"authenticated": True},
    )
