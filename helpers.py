from flask import render_template, redirect, session
import os
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def checkUserInfo(user, email, password, confirmation):
    # Ensure username was submitted
    if not user:
        return "Must provide userName"
    # Ensure email was submitted
    elif not email:
        return "Maust provide email"
    # Ensure passwors was submitted
    elif not password:
        return "Must provide password"
    # Ensure pussword confirmation was submitted
    elif not confirmation:
        return "Must provide pussword confirmatio"
    elif password != confirmation:
        return "Password not match"

    return True
