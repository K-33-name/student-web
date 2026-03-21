from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="tpl", static_folder="static")
app.secret_key = "set_secret"

# ✅ UPDATED DATABASE NAME
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="setdb"
)

cursor = db.cursor()

# HOME
@app.route("/")
def home():
    return render_template("home.html")


# REGISTER
@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        university = request.form.get("university")
        user_class = request.form.get("class")
        age = request.form.get("age")
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        hashed = generate_password_hash(password)

        cursor.execute(
            """INSERT INTO users
            (name, email, university, class, age, mobile, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (name, email, university, user_class, age, mobile, hashed)
        )
        db.commit()

        return redirect("/log")

    return render_template("reg.html")


# LOGIN
@app.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[7], password):
            session["user"] = user
            return redirect("/dash")

        return render_template("log.html", error="Invalid login")

    return render_template("log.html")


# DASHBOARD
@app.route("/dash")
def dash():
    if "user" in session:
        return render_template("dash.html", user=session["user"])
    return redirect("/log")


# LOGOUT
@app.route("/out")
def out():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)