@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        result = c.execute(query).fetchone()

        conn.close()

        if result:
            return "🎉 Flag: flag{SQL_injection_master}"
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')