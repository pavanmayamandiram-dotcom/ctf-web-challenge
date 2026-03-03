from flask import Flask, render_template, request, redirect, session, make_response

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Temporary in-memory user storage
users = {}


# ===================== LOGIN =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ===================== REGISTER =====================
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        # Password match validation
        if password != confirm:
            error = "Passwords do not match!"
            return render_template("register.html", error=error)

        # Username already exists check
        if username in users:
            error = "Username already exists!"
            return render_template("register.html", error=error)

        # Store user
        users[username] = password

        return redirect("/")

    return render_template("register.html")


# ===================== DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("dashboard.html")


# ===================== GAME 1 (Improved CTF Flow) =====================
@app.route("/game1", methods=["GET", "POST"])
def game1():
    role = request.cookies.get("role")

    if not role:
        role = "guest"

    access_granted = False
    message = "Limited Access"

    if request.method == "POST":
        if role == "admin":
            access_granted = True
            message = "Admin Privileges Confirmed"
        else:
            message = "Access Denied - Insufficient Privileges"

    response = make_response(render_template(
        "game1.html",
        role=role,
        access_granted=access_granted,
        message=message
    ))

    # Always ensure cookie exists
    response.set_cookie("role", role)

    return response


# ===================== RUN APP =====================
if __name__ == "__main__":
    app.run()