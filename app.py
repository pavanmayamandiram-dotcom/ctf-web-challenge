from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Vulnerable query (SQL Injection)
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        result = c.execute(query).fetchone()

        conn.close()

        if result:
            return "🎉 Flag: flag{SQL_injection_master}"
        else:
            return "Invalid credentials"

    return render_template('login.html')

init_db()

if __name__ == '__main__':
    app.run()