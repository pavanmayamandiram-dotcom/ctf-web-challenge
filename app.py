from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# ---------------------------
# Initialize Database
# ---------------------------
def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """)
        # Default admin user
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        conn.commit()
        conn.close()

# ---------------------------
# Login Route (Vulnerable)
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # 🚨 Vulnerable SQL Query (SQL Injection)
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        result = c.execute(query).fetchone()

        conn.close()

        if result:
            return """
            <div style='background:black;color:#00ff00;font-family:monospace;padding:40px;height:100vh'>
            <h1>🎉 ACCESS GRANTED</h1>
            <h2>Flag: flag{SQL_injection_master}</h2>
            </div>
            """
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

# ---------------------------
# Start App
# ---------------------------
init_db()

if __name__ == '__main__':
    app.run()