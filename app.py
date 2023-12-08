from flask import Flask, render_template, request
import pymssql

app = Flask(__name__)

MSSQL_USER = "SwiftCabApp"
MSSQL_USERPASS = "67Syjg:D4^uS"
MSSQL_DB = "SwiftDB"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username, password = request.json["username"], request.json["password"]
        # with mssql.connect("localhost", MSSQL_USER, MSSQL_USERPASS, MSSQL_DB) as conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute("SELECT LocationName FROM LOCATIONS", )
        #         locations = cursor.fetchall()
        return render_template("login.html")