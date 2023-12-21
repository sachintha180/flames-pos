from flask import Flask, render_template, request, session
from models import db, User
from helpers import generate_response, validate_attributes
from flask_bcrypt import generate_password_hash, check_password_hash
import enums
import traceback

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flames.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "6225ca4ab01df210894501e8958e8611a7dd5ddf73f2c9cbb8064b1afd52bb1f"

# initialize models.py SQLAlchemy object
db.init_app(app)

# note: db.create_all() only creates models if they don't exist
with app.app_context():
    db.create_all()


# note: /initialize route and its child routes are NOT PUBLICLY visible
@app.route("/initialize", methods=["GET", "POST"])
def initialize():
    if request.method == "GET":
        return render_template("initialize.html")
    else:
        # validate the presence of username and password attributes in payload
        response = validate_attributes(request.json, ["username", "password"])
        if response.status_code != 200:
            return response

        # verify the provided credentials against the superadmin's credentials
        superadmin_creds = {
            "username": "superadmin",
            "password": "admin123",
        }
        response = validate_attributes(
            request.json, request.json.keys(), superadmin_creds
        )
        if response.status_code != 200:
            return response

        # return the admin user's default credentials
        admin_default = {
            "username": "admin",
            "password": "Pi$$a@456",
            "name": "Flames POS Administrator",
            "mobile_no": "0121231234",
            "role": "admin",
        }
        return generate_response(
            status_code=200,
            message="Login successful",
            action="You are now authenticated as superadmin",
            data={"admin_default": admin_default, "flag": True},
        )


@app.route("/add_admin", methods=["POST"])
def addAdmin():
    if request.method == "POST":
        try:
            # validate the presence of User model attributes in payload
            response = validate_attributes(
                request.json, ["username", "password", "name", "mobile_no"]
            )
            if response.status_code != 200:
                return response

            # check if provided username already exists
            try:
                db.session.execute(
                    db.select(User).filter(User.username == request.json["username"])
                ).scalar_one()
            except:
                # create and insert admin into database
                admin = User(
                    username=request.json["username"],
                    password=generate_password_hash(request.json["password"]),
                    name=request.json["fullname"],
                    mobile_no=request.json["mobile_no"],
                    role=enums.UserRole.admin.value,
                )
                db.session.add(admin)
                db.session.commit()
            else:
                return generate_response(
                    status_code=400,
                    message="Username already exists",
                    action="Please try again with a different username",
                    data={"flag": False},
                )

        except Exception:
            return generate_response(
                status_code=400,
                message="Failed to add adminstrator",
                action=f"{traceback.format_exc()}",
                data={"flag": False},
            )

        # otherwise, return success JSON
        return generate_response(
            status_code=200,
            message="Successfully added admin",
            action=f"You have now added the admin '{request.json['username']}'",
            data={"flag": True},
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # validate the presence of username and password attributes in payload
        response = validate_attributes(request.json, ["username", "password"])
        if response.status_code != 200:
            return response

        # otherwise, get username from database + save to session variable
        try:
            user = db.session.execute(
                db.select(User).filter(User.username == request.json["username"])
            ).scalar_one()
        except:
            return generate_response(
                status_code=404,
                message="Username not found",
                action="Please register your account via an administrator",
                data={"flag": False},
            )

        session["username"] = request.json["username"]
        print(user)

        # verify password against saved password
        if not check_password_hash(user.password, request.json["password"]):
            return generate_response(
                status_code=401,
                message="Authentication failed",
                action="Incorrect password, please try again",
                data={"flag": False},
            )

        # return success JSON
        return generate_response(
            status_code=200,
            message="Login successful",
            action="You are now logged in",
            data={"flag": True},
        )


if __name__ == "__main__":
    app.run(debug=True)
