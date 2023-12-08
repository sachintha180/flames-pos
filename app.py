import json
from flask import Flask, Response, render_template, request

app = Flask(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username, password = request.json["username"], request.json["password"]
        response = {
            "authenticated": True
        }
        return Response(response=json.dumps(response), status=200, mimetype="application/json")
