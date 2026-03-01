# Offenzo CTF Theme Update
from flask import Flask, render_template, request
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

        # Insert default admin user
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecret123')")

        conn.commit()
        conn.close()

# -----------------------------
# Login Route (CTF Challenge)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # ⚠️ Intentionally Vulnerable Query (SQL Injection)
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        result = c.execute(query).fetchone()

        conn.close()

        if result:
            return """
            <h1 style='color:green;text-align:center;margin-top:100px;'>
            🎉 Access Granted <br><br>
            Flag: flag{Offenzo_SQL_Injection_Master}
            </h1>
            """
        else:
            return render_template("login.html", error="Invalid user name or password")

    return render_template("login.html")


# -----------------------------
# Run App
# -----------------------------
init_db()

if __name__ == "__main__":
    app.run()