import os
import json
from flask import Flask, render_template, request, redirect, session, make_response

app = Flask(name)
app.secret_key = "supersecretkey"

===================== USER STORAGE =====================

USERS_FILE = "users.json"

try:
with open(USERS_FILE, "r") as f:
users = json.load(f)
except:
users = {}

===================== LOGIN =====================

@app.route("/", methods=["GET", "POST"])
def login():
if request.method == "POST":
username = request.form["username"]
password = request.form["password"]

    if username in users and users[username] == password:
        session["username"] = username
        session["game1_solved"] = False
        return redirect("/dashboard")
    else:
        return render_template("login.html", error="Invalid username or password")

return render_template("login.html")

===================== REGISTER =====================

@app.route("/register", methods=["GET", "POST"])
def register():
if request.method == "POST":

    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm_password"]

    if password != confirm:
        return render_template("register.html", error="Passwords do not match!")

    if username in users:
        return render_template("register.html", error="Username already exists!")

    users[username] = password

    # Save users permanently
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

    return redirect("/")

return render_template("register.html")

===================== DASHBOARD =====================

@app.route("/dashboard")
def dashboard():

if "username" not in session:
    return redirect("/")

return render_template(
    "dashboard.html",
    game1_solved=session.get("game1_solved", False)
)

===================== GAME 1 =====================

@app.route("/game1", methods=["GET", "POST"])
def game1():

role = request.cookies.get("role", "guest")

access_granted = False
message = "Access Restricted"

if request.method == "POST":

    if role == "admin":
        access_granted = True
        message = "Admin Privileges Confirmed"
    else:
        message = "Access Denied"

response = make_response(render_template(
    "game1.html",
    role=role,
    access_granted=access_granted,
    message=message
))

if not request.cookies.get("role"):
    response.set_cookie("role", "guest")

return response

===================== FLAG SUBMISSION =====================

@app.route("/submit_flag1", methods=["POST"])
def submit_flag1():

submitted_flag = request.form["flag"].strip()
correct_flag = "FLAG{broken_access_control_cookie}"

if submitted_flag == correct_flag:

    session["game1_solved"] = True
    return render_template("success1.html")

return render_template(
    "game1.html",
    role="guest",
    access_granted=True,
    message="Incorrect Flag. Try Again."
)

===================== GAME 2 (SQL Injection) =====================

@app.route("/game2", methods=["GET", "POST"])
def game2():

if "username" not in session:
    return redirect("/")

if not session.get("game1_solved"):
    return redirect("/dashboard")

error = None
flag = None

if request.method == "POST":

    username = request.form.get("username")
    password = request.form.get("password")

    # Simulated vulnerable SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    # SQL Injection vulnerability
    if username and "admin' --" in username:
        flag = "FLAG{sql_authentication_bypass}"
    else:
        error = "Invalid username or password"

return render_template("game2.html", error=error, flag=flag)

===================== RUN (Render Compatible) =====================

if name == "main":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)