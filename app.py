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


# ===================== GAME 1 (Cookie Vulnerability) =====================
@app.route("/game1")
def game1():
    role = request.cookies.get("role")

    is_admin = role == "admin"

    response = make_response(render_template("game1.html", is_admin=is_admin))

    # Set default role
    if not role:
        response.set_cookie("role", "guest")

    return response


# ===================== RUN APP =====================
if __name__ == "__main__":
    app.run()