from flask import Flask, jsonify, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from base import Base

# IMPORTANT:
#   Follow these steps during the first run:
#    (1) Run app.py FIRST on / route and stop the server
#    (2) Run setup.py next (after instance/flames.db has initialized)
#    (3) Restart app.py and continue as usual

# TODO: Running `python app.py` doesn't work due to:
#       "The current Flask app is not registered with this 'SQLAlchemy' instance. Did you forget to call 'init_app'"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flames.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "6225ca4ab01df210894501e8958e8611a7dd5ddf73f2c9cbb8064b1afd52bb1f"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

from models import *

# note: db.create_all() only creates models if they don't exist
with app.app_context():
    db.create_all()


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # check #1: username not provided in payload
        try:
            username = request.json["username"]
        except KeyError:
            return generate_response(
                status_code=400,
                message="Username not received",
                action="Please refresh your page and try logging in again",
                data={"authenticated": False},
            )

        # check #2: password not provided in payload
        try:
            password = request.json["password"]
        except KeyError:
            return generate_response(
                status_code=400,
                message="Password not received",
                action="Please refresh your page and try logging in again",
                data={"authenticated": False},
            )

        # check #3: username empty in payload
        if username is None:
            return generate_response(
                status_code=400,
                message="Empty username",
                action="Please enter a valid username",
                data={"authenticated": False},
            )

        # check #4: password empty in payload
        if password is None:
            return generate_response(
                status_code=400,
                message="Empty password",
                action="Please enter a valid password",
                data={"authenticated": False},
            )

        # otherwise: get username from database
        try:
            user = db.session.execute(
                db.select(User).filter(User.username == username)
            ).scalar_one()
        except exc.NoResultFound:
            return generate_response(
                status_code=404,
                message="Username not found",
                action="Please register your account via an administrator",
                data={"authenticated": False},
            )
        else:
            session["username"] = username

        return generate_response(
            status_code=200,
            message="Login successful",
            action="You are now logged in",
            data={"authenticated": True},
        )


if __name__ == "__main__":
    app.run(debug=True)
