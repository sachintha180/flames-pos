from flask import Flask, render_template, request, session
from models import db, User
from helpers import generate_response, validate_attributes
from flask_bcrypt import generate_password_hash, check_password_hash
import enums

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")

# initialize models.py SQLAlchemy object
db.init_app(app)

# note: db.create_all() only creates models if they don't exist
with app.app_context():
    db.create_all()


# note: /initialize route is NOT PUBLICLY visible
@app.route("/initialize", methods=["GET", "POST"])
def initialize():
    if request.method == "GET":
        return render_template("initialize.html")
    else:
        # verify the provided credentials against the superadmin's credentials
        response = validate_attributes(
            request.json,
            ["username", "password"],
            app.config.get("SUPERADMIN"),
        )
        if response.status_code != 200:
            return response

        # return the owner's default credentials
        return generate_response(
            status_code=200,
            message="Login successful",
            action="You are now authenticated as superadmin",
            data={"owner_default": app.config.get("OWNER_DEFAULT"), "flag": True},
        )


# note: /add_owner route is NOT PUBLICLY visible
@app.route("/add_owner", methods=["POST"])
def addOwner():
    if request.method == "POST":
        # validate the presence of User model attributes in payload
        response = validate_attributes(
            request.json, ["username", "password", "fullname", "mobile_no"]
        )
        if response.status_code != 200:
            return response

        # query username in database
        try:
            matched_users = (
                db.session.scalars(
                    db.select(User).where(User.username == request.json["username"])
                )
                .all()
            )
            print(matched_users)
        except Exception as e:
            return generate_response(
                status_code=400,
                message="Failed to check owner",
                action=f"Server responded with error: {e[:app.config.get('MAX_ERROR_LENGTH')]}",
                data={"flag": False},
            )

        # check if provided username already exists
        if len(matched_users) > 0:
            return generate_response(
                status_code=400,
                message="Owner already exists",
                action="Please try again with a different username",
                data={"flag": False},
            )

        # otherwise, create and insert owner into database
        try:
            owner = User(
                username=request.json["username"],
                password=generate_password_hash(request.json["password"]),
                fullname=request.json["fullname"],
                mobile_no=request.json["mobile_no"],
                role=enums.UserRole.owner.value,
            )
            db.session.add(owner)
            db.session.commit()
        except Exception as e:
            return generate_response(
                status_code=400,
                message="Failed to add owner",
                action=f"Server responded with error: {e[:app.config.get('MAX_ERROR_LENGTH')]}",
                data={"flag": False},
            )

        # otherwise, return success JSON
        return generate_response(
            status_code=200,
            message="Successfully added owner",
            action=f"You have now added the owner '{request.json['username']}'",
            data={"flag": True},
        )


# note: /reset_db route is NOT PUBLICLY visible
@app.route("/reset_db", methods=["POST"])
def resetDB():
    if request.method == "POST":
        # verify the provided credentials against the superadmin's credentials
        response = validate_attributes(
            request.json,
            ["username", "password"],
            app.config.get("SUPERADMIN"),
        )
        if response.status_code != 200:
            return response

        # delete and re-initialize schema
        try:
            db.drop_all()
            db.create_all()
        except Exception as e:
            return generate_response(
                status_code=400,
                message="Failed to reset database",
                action=f"Server responded with error: {e[:app.config.get('MAX_ERROR_LENGTH')]}",
                data={"flag": False},
            )

        # return success JSON
        return generate_response(
            status_code=200,
            message="Successfully reset database",
            action=f"You have now reset the database",
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
    app.run()
