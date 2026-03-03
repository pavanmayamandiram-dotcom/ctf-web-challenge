from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home Route (Login Page)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple demo login (you can change later)
        if username == "admin" and password == "admin":
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return """
    <h1 style='color:lime; background:black; padding:40px; text-align:center;'>
    Welcome to Offenzo CTF Dashboard 🚀
    </h1>
    """


if __name__ == "__main__":
    app.run(debug=True)