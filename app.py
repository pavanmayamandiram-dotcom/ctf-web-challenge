from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Create users table
        c.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        """)

        # Default user
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")

        conn.commit()
        conn.close()


# -----------------------------
# Login Route (VULNERABLE)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # 🚨 Intentionally vulnerable SQL query
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        result = c.execute(query).fetchone()

        conn.close()

        if result:
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# -----------------------------
# Dashboard Route
# -----------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# Challenge 1 (Vulnerable)
# -----------------------------
@app.route("/challenge1")
def challenge1():
    return render_template("challenge1.html")


# -----------------------------
# Flag Route (Hidden)
# -----------------------------
@app.route("/flag")
def flag():
    return "🏴 Flag: flag{SQL_injection_master}"


# -----------------------------
# Start App
# -----------------------------
init_db()

if __name__ == "__main__":
    app.run(debug=True)