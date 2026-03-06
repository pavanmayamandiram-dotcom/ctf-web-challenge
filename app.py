import os
import json
from flask import Flask, render_template, request, redirect, session, make_response

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ================= USER STORAGE =================
USERS_FILE = "users.json"

try:
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
except:
    users = {}

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:

            session["username"] = username

            # Only initialize once
            if "game1_solved" not in session:
                session["game1_solved"] = False

            return redirect("/dashboard")

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ================= REGISTER =================
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

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

        return redirect("/")

    return render_template("register.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        game1_solved=session.get("game1_solved", False)
    )


# ================= GAME 1 (Broken Access Control) =================
@app.route("/game1", methods=["GET", "POST"])
def game1():

    role = request.cookies.get("role", "guest")

    access_granted = False
    message = "Access Restricted"

    if request.method == "POST":

        if role == "admin":

            access_granted = True
            message = "Admin Privileges Confirmed"

            # Unlock Game 2
            session["game1_solved"] = True

            return redirect("/dashboard")

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


# ================= GAME 2 (SQL Injection) =================
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
        if username and "admin" in username:
            flag = "FLAG{sql_authentication_bypass}"
        else:
            error = "Invalid username or password"

    return render_template("game2.html", error=error, flag=flag)


# ================= RUN APP =================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)