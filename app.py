from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "offenzo_secret_key"

# ---------------- DATABASE CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- USER MODEL ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username  # session protection

            # Vulnerable cookie (for Game 1)
            response = make_response(redirect(url_for("dashboard")))
            response.set_cookie("role", "user")  # intentionally vulnerable
            return response
        else:
            flash("Invalid username or password")

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!")
            return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ---------------- GAME 1 ----------------
@app.route("/game1")
def game1():
    if "user" not in session:
        return redirect(url_for("login"))

    role = request.cookies.get("role")

    # Intentional vulnerability:
    # We TRUST client-side cookie without verification
    if role == "admin":
        return """
        <div style='background:black; color:lime; padding:50px; text-align:center;'>
            <h1>FLAG{broken_access_control}</h1>
            <p>You escalated privileges successfully.</p>
        </div>
        """
    else:
        return """
        <div style='background:black; color:red; padding:50px; text-align:center;'>
            <h2>Access Denied. Admins Only.</h2>
            <p>Current role: user</p>
        </div>
        """

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    response = make_response(redirect(url_for("login")))
    response.set_cookie("role", "", expires=0)
    return response

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)