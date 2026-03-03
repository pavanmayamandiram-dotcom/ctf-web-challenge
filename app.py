from flask import Flask, render_template, request, redirect, session, make_response

app = Flask(__name__)
app.secret_key = "supersecretkey"

users = {}

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/game1")
def game1():
    role = request.cookies.get("role")

    is_admin = role == "admin"

    response = make_response(render_template("game1.html", is_admin=is_admin))

    if not role:
        response.set_cookie("role", "guest")

    return response

if __name__ == "__main__":
    app.run()