from tempfile import mkdtemp
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, checkUserInfo
from models.user import Users
from models.topic import Topics
from models.vocabulary import Vocabularys
from models.progress import Progress
from models.db import db

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnglish.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Creare db
with app.app_context():
    db.create_all()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["email"].lower()
        userPassword = request.form["password"]

        # Check password lenght
        if len(userPassword) <= 5:
            return apology("Password is too short", 400)

        userCount = Users.query.filter_by(email=userEmail).count()
        if userCount == 1:
            user = Users.query.filter_by(email=userEmail)
            if check_password_hash(user[0].password, userPassword):
                session["user_id"] = user[0].id
                return redirect("/")
            else:
                return apology("Password not match", 400)
        else:
            return apology("Email not match", 400)
    else:
        # GET
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        userName = request.form.get("username")
        userEmail = request.form.get("email").lower()
        userPassword = request.form.get("password")
        userConfirmPassword = request.form.get("confirmation")
        # Check lenght of password
        if len(userPassword) <= 5:
            return apology("Password is too short", 400)

        if checkUserInfo(userName, userEmail, userPassword, userConfirmPassword) == True:
            hashPassword = generate_password_hash(userPassword)
            newUser = Users(name=userName, email=userEmail,
                            password=hashPassword)
            try:
                db.session.add(newUser)
                db.session.commit()
                session["user_id"] = newUser.id
                print(session["user_id"])
                print(newUser.id)
                return redirect("/")
            except IntegrityError as e:
                # Check if User already exist in DB by email
                # return errorhandler(e) alternative variant from server eror
                return apology("Email already exist", 400)
        else:
            return apology(checkUserInfo(userName, userEmail, userPassword, userConfirmPassword))
    else:
        # GET
        return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
