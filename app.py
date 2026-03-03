from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            response = make_response(redirect(url_for("dashboard")))
            response.set_cookie("role", "user")  # vulnerable part
            return response
        else:
            flash("Invalid username or password")

    return render_template("login.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!")
            return redirect(url_for("login"))

    return render_template("register.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Game 1
@app.route("/game1")
def game1():
    role = request.cookies.get("role")

    if role == "admin":
        return "<h1 style='color:lime;'>FLAG{broken_access_control}</h1>"
    else:
        return "<h2 style='color:red;'>Access Denied. Admins Only.</h2>"

if __name__ == "__main__":
    app.run(debug=True)