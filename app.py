from flask import Flask, render_template, request, redirect, session, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "ultra_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- DATABASE ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect("/login")

# -------- REGISTER --------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "User already exists"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

# -------- LOGIN --------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid username or password"

    return render_template("login.html")

# -------- DASHBOARD --------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

# -------- GAME 1 (VULNERABLE) --------

@app.route("/game1")
def game1():
    if "user" not in session:
        return redirect("/login")

    role = request.cookies.get("role")

    if role == "admin":
        return "FLAG{cookie_admin_access_success}"
    else:
        response = make_response(render_template("game1.html"))
        response.set_cookie("role", "guest")
        return response

# -------- OTHER GAMES --------

@app.route("/game2")
def game2():
    return render_template("game2.html")

@app.route("/game3")
def game3():
    return render_template("game3.html")

@app.route("/game4")
def game4():
    return render_template("game4.html")

@app.route("/game5")
def game5():
    return render_template("game5.html")

@app.route("/game6")
def game6():
    return render_template("game6.html")

@app.route("/game7")
def game7():
    return render_template("game7.html")

if __name__ == "__main__":
    app.run()