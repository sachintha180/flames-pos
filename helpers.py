"""
helpers.py (docstring generated by DuetAI).

This module contains helper functions for the Flames POS application.
"""

import random
from flask import jsonify, session, redirect, url_for, request
from functools import wraps
import re


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


def validate_attributes(attribute_dict, attribute_list, target_dict=None):
    """Validate a list of attributes in a dictionary, and optionally against a dictionary of target attributes.

    Args:
        attribute_dict (dict): the dictionary of attribute names and values to validate
        attribute_list (list): the list of attribute names
        target_dict (dict): the dictionary of target attributes to validate against
    Returns:
        response (Response): the JSON response with a status code, message, action, and data
    """

    for attribute in attribute_list:
        # check if attribute is present in dictionary (i.e. response JSON dictionary)
        try:
            attribute_dict[attribute]
        except KeyError:
            return generate_response(
                status_code=400,
                message=f"{attribute.capitalize()} not received",
                action="Please refresh your page and try again",
                data={"flag": False},
            )

        # if found, check if attribute is falsy
        if not attribute_dict[attribute]:
            return generate_response(
                status_code=400,
                message=f"Empty {attribute.capitalize()}",
                action=f"Please enter a valid {attribute}",
                data={"flag": False},
            )

        # if not None, check if it matches a provided target (if provided)
        if target_dict is not None:
            if attribute_dict[attribute] != target_dict[attribute]:
                return generate_response(
                    status_code=401,
                    message="Authentication failed",
                    action=f"Please enter the correct {attribute}",
                    data={"flag": False},
                )

    # otherwise, return simple success response (since truthy responses are customized to the caller)
    return generate_response(
        status_code=200,
        message="Success",
        action="",
        data={"flag": True},
    )


def verify_user(user_dict):
    length_constraints = {
        "username": [4, 20],
        "password": [8, 20],
        "fullname": [10, 50],
        "mobile_no": [10, 10],
    }

    mobile_no_regex = re.compile(r"[0-9]{10}")

    for attribute, value in user_dict.items():
        if len(value) < length_constraints[attribute][0]:
            return generate_response(
                status_code=400,
                message=f"{attribute.capitalize()} too short",
                action=f"Please enter a {attribute} with at least {length_constraints[attribute][0]} characters",
                data={"flag": False},
            )

        elif len(value) > length_constraints[attribute][1]:
            return generate_response(
                status_code=400,
                message=f"{attribute.capitalize()} too long",
                action=f"Please enter a {attribute} with at most {length_constraints[attribute][1]} characters",
                data={"flag": False},
            )

        elif attribute == "mobile_no" and re.fullmatch(mobile_no_regex, value) is None:
            return generate_response(
                status_code=400,
                message=f"Invalid mobile number",
                action=f"Please enter a valid mobile number",
                data={"flag": False},
            )


def print_order_bill(order, totals, items):
    return

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return decorated_function


def get_random_quote():
    quotes = [
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "Don't be afraid to give up the good to go for the great. - John D. Rockefeller",
        "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
        "The only place where success comes before work is in the dictionary. - Vidal Sassoon",
        "Opportunities don't happen. You create them. - Chris Grosser",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The secret of getting ahead is getting started. - Mark Twain",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is stumbling from failure to failure with no loss of enthusiasm. - Winston S. Churchill",
        "It's not about ideas. It's about making ideas happen. - Scott Belsky",
        "Success is not in what you have, but who you are. - Bo Bennett",
        "If you are not willing to risk the usual, you will have to settle for the ordinary. - Jim Rohn",
    ]
    return random.choice(quotes)
