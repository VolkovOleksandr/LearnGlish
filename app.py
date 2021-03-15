from tempfile import mkdtemp
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, checkUserInfo
from models.user import Users, topic_identifier
from models.topic import Topics
from models.vocabulary import Vocabularys
from models.progress import Progress
from models.topicSchema import TopicSchema
from models.vocabularySchema import VocabularySchema
from models.db import db
from models.ma import ma

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnglish.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

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


@app.route("/study/<string:topic_id>")
@login_required
def study(topic_id):
    topicTitle = Topics.query.get(topic_id)
    userId = session["user_id"]
    vocab_schema = VocabularySchema(many=True)
    vocabs = Vocabularys.query.filter(and_(
        Vocabularys.user_id == userId, Vocabularys.topic_id == topic_id)).all()
    jsonVocabs = vocab_schema.dump(vocabs)
    return render_template("study.html", topicTitle=topicTitle, vocabs=vocabs)


@app.route("/study/word/add", methods=["POST"])
@login_required
def addWord():
    # Get gata from user
    topicId = request.form["topicId"]
    originWord = request.form["wordOrigin"]
    translateWord = request.form["wordTranslate"]
    userId = session["user_id"]
    # Chec if all fields are entered
    if not originWord or not translateWord:
        flash("Origin word or translate not entered. Please try again")
        return redirect("/study/{}".format(topicId))
    # Add word to DB
    newWord = Vocabularys(user_id=userId, topic_id=topicId,
                          type="word", origin=originWord, translate=translateWord)
    db.session.add(newWord)
    db.session.commit()
    flash("Word successfully added")
    return redirect("/study/{}".format(topicId))


@app.route("/study/word/edit", methods=["POST"])
@login_required
def editWord():
    # Get gata from user
    topicId = request.form["topicId"]
    wordId = request.form["wordId"]
    originWord = request.form["wordOrigin"]
    translateWord = request.form["wordTranslate"]
    userId = session["user_id"]
    # Check if all fields are entered
    if not originWord or not translateWord:
        flash("Origin word or translate not entered. Please try again")
        return redirect("/study/{}".format(topicId))
    # Edit word in DB
    vocab = Vocabularys.query.get(wordId)
    vocab.origin = originWord
    vocab.translate = translateWord
    db.session.commit()
    flash("Word successfully eddited")
    return redirect("/study/{}".format(topicId))


@app.route("/study/word/delete", methods=["POST"])
@login_required
def deleteWord():
    topicId = request.form["topicId"]
    wordId = request.form["deleteId"]
    wordDB = Vocabularys.query.get(wordId)
    db.session.delete(wordDB)
    db.session.commit()
    flash("Word successfully deleted")
    return redirect("/study/{}".format(topicId))


@app.route("/topics")
@login_required
def topics():
    # Creare schema for Topic
    topic_schema = TopicSchema(many=True)
    user = Users.query.get(session["user_id"])
    # Get all topics from DB
    topics = Topics.query.join(topic_identifier).join(Users).filter(
        (topic_identifier.c.user_id == user.id)).all()

    jsonTopics = topic_schema.dump(topics)
    # TODO Pagination and each group-list should be limited by 10
    # Return data to html
    return render_template("topics.html", userTopics=jsonTopics)


@app.route("/topics/add", methods=["POST"])
@login_required
def addNewTopic():
    topicInput = request.form["topic"]
    # Get user and check if topick in DB
    currentUser = Users.query.get(session["user_id"])
    topicId = Topics.query.filter_by(topic=topicInput).first()
    if topicId:
        # If topic already in DB just append to current user topic_id
        currentUser.topics.append(Topics.query.get(topicId.id))
        db.session.add(currentUser)
        db.session.commit()
        flash('You were successfully add topick')
        return redirect("/topics")
    else:
        # If not create new topic
        newTopic = Topics(topic=topicInput)
        db.session.add(newTopic)
        currentUser.topics.append(newTopic)
        db.session.add(currentUser)
        db.session.commit()
        flash('You were successfully add new topick')
        return redirect("/topics")


@app.route("/study/topic/edit", methods=["POST"])
@login_required
def editTopic():
    # Get gata from user
    topicId = request.form["topicId"]
    topicTitle = request.form["topicEdit"]
    # Get data from DB and make changes
    topicDB = Topics.query.get(topicId)
    topicDB.topic = topicTitle
    db.session.commit()
    flash("Topick successfully changed")
    return redirect("/study/{}".format(topicId))


@app.route("/study/topic/delete", methods=["POST"])
@login_required
def deleteTopic():
    # Get gata from user
    topicId = request.form["topicId"]
    # Get data from DB and delete
    topicDB = Topics.query.get(topicId)
    db.session.delete(topicDB)
    db.session.commit()
    flash("Topick successfully deleted")
    return redirect("/topics")


@app.route("/topicSearch", methods=["POST"])
@login_required
def topicSearch():
    # Creare schema for Topic
    topic_schema = TopicSchema(many=True)
    # Get data from user form
    dataFromForm = request.get_json()
    searchQueryLike = "%{}%".format(dataFromForm)
    # Query data from DB
    topics = Topics.query.filter(Topics.topic.like(searchQueryLike)).all()
    jsonTopics = topic_schema.dump(topics)
    # Return data to datalist for user
    return jsonify(jsonTopics)


@app.route("/study/getWordById", methods=["POST"])
@login_required
def getWordById():
    # Creare schema for Vocabulary
    vocab_schema = VocabularySchema()
    # Get data from user form
    dataFromForm = request.get_json()
    # Query data from DB
    vocab = Vocabularys.query.get(dataFromForm)
    jsonVocab = vocab_schema.dump(vocab)
    # Return data to datalist for user
    return jsonify(jsonVocab)


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
