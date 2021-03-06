from os import sendfile
from tempfile import mkdtemp, tempdir
from flask import Flask, flash, json, redirect, render_template, request, session, jsonify
from flask_session import Session
import flask_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import random

from helpers import apology, login_required, checkUserInfo, percent
from models.user import Users, topic_identifier
from models.topic import Topics
from models.vocabulary import Vocabularys
from models.progress import Progress
from models.news import News
from models.topicSchema import TopicSchema
from models.vocabularySchema import VocabularySchema
from models.progressSchema import ProgressSchema
from models.userSchema import UserSchema
from models.newsSchema import NewsSchema
from models.db import db
from models.ma import ma

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnglish.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)
# Jinja filters
app.jinja_env.filters["percent"] = percent

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
    news = News.query.all()
    newsSchema = NewsSchema(many=True)
    newsJson = newsSchema.dump(news)
    newsArray = []

    for element in newsJson:
        newsJsonList = {
            "title": "",
            "id": 0,
            "short": ""
        }
        newsJsonList["title"] = element["title"]
        newsJsonList["id"] = element["id"]
        short = element["text"][:120]
        newsJsonList["short"] = short
        newsArray.append(newsJsonList)
    return render_template("index.html", newsList=newsArray)

# admin control panel


@app.route("/admin")
@login_required
def admin():
    if(session["email"] == "admin@admin"):
        news = News.query.filter(
            News.user_id == session["user_id"]).all()
        newsSchema = NewsSchema(many=True)
        newsJson = newsSchema.dump(news)
        # Get all users
        users = Users.query.all()
        usersShema = UserSchema(many=True)
        usersJson = usersShema.dump(users)
        return render_template("admin.html", newsList=newsJson, usersList=usersJson)
    else:
        return apology("Not permitted", 400)

# Add news


@app.route("/admin/news/add", methods=["POST"])
@login_required
def addNews():
    title = request.form["newsTitle"]
    text = request.form["newsText"]
    news = News(user_id=session["user_id"], title=title, text=text)
    try:
        db.session.add(news)
        db.session.commit()
        flash("News succsessfuly added")
        return redirect("/admin")
    except IntegrityError as e:
        # Check if News already exist in DB by title
        # return errorhandler(e) alternative variant from server eror
        return apology("News already exist", 400)

# Schow news by Id


@app.route("/readNews/<string:newsId>")
def readNews(newsId):
    news = News.query.get(newsId)
    newSchema = NewsSchema()
    newsJson = newSchema.dump(news)
    return render_template("news.html", newsObject=newsJson)

# Delete news by id


@app.route("/news/delete", methods=["POST"])
@login_required
def newsDelete():
    newsId = request.form["deleteNewsId"]
    news = News.query.get(newsId)
    db.session.delete(news)
    db.session.commit()
    flash("News sucsessfuly deleted !")
    return redirect("/admin")


# Clean statistics

@app.route("/statistics/delete", methods=["POST"])
@login_required
def statisticDelete():
    topicId = request.form["deletedTopicId"]
    # Erase user progress for current topic Id
    progress_schema = ProgressSchema(many=True)
    userProgress = Progress.query.filter(
        and_(Progress.user_id == session["user_id"], Progress.topic_id == topicId)).all()
    progressToJSON = progress_schema.dump(userProgress)
    # Check if user has progress in DB
    if len(progressToJSON) == 0:
        flash("No statistics for erasing")
        return redirect("/statistics")
    # Eraising data in DB
    for item in userProgress:
        item.attempts = 0
        item.success = 0
        db.session.commit()
    flash("Topic sucsessfuly eraised!")
    return redirect("/statistics")


@ app.route("/statistics")
@ login_required
def statistics():
    userId = session["user_id"]
    # Get data from Vocabulary and save to JSON object
    userStats = {
        "totalWordsAndPhrases": [],
        "totalAttemptsAndSuccess": []
    }
    # DB query
    vocabWords = Vocabularys.query.filter(and_(
        Vocabularys.user_id == userId, Vocabularys.type == "word")).all()
    vocabPhrases = Vocabularys.query.filter(and_(
        Vocabularys.user_id == userId, Vocabularys.type == "phrase")).all()
    userStats["totalWordsAndPhrases"].append(len(vocabWords))
    userStats["totalWordsAndPhrases"].append(len(vocabPhrases))
    # Count total amount of Attempts and success
    progress_schema = ProgressSchema(many=True)
    userProgress = Progress.query.filter(
        Progress.user_id == userId).all()
    userProgresJson = progress_schema.dump(userProgress)
    attemptCounter = 0
    successCounter = 0
    for element in userProgresJson:
        attemptCounter += element["attempts"]
        successCounter += element["success"]
    userStats["totalAttemptsAndSuccess"].append(attemptCounter)
    userStats["totalAttemptsAndSuccess"].append(successCounter)
    # Convert object to JSON
    userStatsJson = json.dumps(userStats)
    progressArray = []

    # Creare schema for Topic
    topic_schema = TopicSchema(many=True)
    user = Users.query.get(session["user_id"])
    # Get all topics from DB by UserId
    topics = Topics.query.join(topic_identifier).join(Users).filter(
        (topic_identifier.c.user_id == user.id)).all()
    jsonTopics = topic_schema.dump(topics)
    # Create schema for Progress for each topic
    progress_schema = ProgressSchema(many=True)
    for topic in jsonTopics:
        progressInfoObj = {
            "topicId": 0,
            "topic": "",
            "attempts": 0,
            "success": 0
        }
        countProgressAttempts = 0
        countProgressSuccess = 0
        progressInfoObj["topicId"] = topic["id"]
        progressInfoObj["topic"] = topic["topic"]
        # Get statistic for each topic
        userProgress = Progress.query.filter(and_(
            Progress.user_id == userId, Progress.topic_id == topic["id"])).all()
        progressToJSON = progress_schema.dump(userProgress)
        for element in progressToJSON:
            countProgressAttempts += element["attempts"]
            countProgressSuccess += element["success"]
        progressInfoObj["attempts"] = countProgressAttempts
        progressInfoObj["success"] = countProgressSuccess
        progressArray.append(progressInfoObj)

    # Get data for setting Tab
    userSchema = UserSchema()
    userInfo = Users.query.get(userId)
    userInfoJson = userSchema.dump(userInfo)

    return render_template("statistics.html", userTotalStat=userStatsJson, progressInfo=progressArray, userSettings=userInfoJson)

# change user name


@ app.route("/settings/changeName", methods=["POST"])
@ login_required
def changeName():
    userId = request.form["userId"]
    userNewName = request.form["changeName"]
    userChanges = Users.query.get(userId)
    userChanges.name = userNewName
    db.session.commit()
    flash("Your name successfuly changed")
    return redirect("/statistics")

# change user email


@ app.route("/settings/changeEmail", methods=["POST"])
@ login_required
def changeEmail():
    userId = request.form["userId"]
    userNewEmail = request.form["changeEmail"]
    userChanges = Users.query.get(userId)
    userChanges.email = userNewEmail
    db.session.commit()
    flash("Your email successfuly changed")
    return redirect("/statistics")

# Change user password


@ app.route("/settings/changePassword", methods=["POST"])
@ login_required
def changePassword():
    userId = request.form["userId"]
    userNewPassword = request.form["changePassword"]
    userOldPassword = request.form["oldPassword"]
    userChanges = Users.query.get(userId)
    if check_password_hash(userChanges.password, userOldPassword) and (len(userNewPassword) > 5):
        flash("Password successfuly changed")
        userChanges.password = generate_password_hash(userNewPassword)
        db.session.commit()
    else:
        return apology("Old password doen't match or new password too short", 400)

    return redirect("/statistics")


@ app.route("/study/startQuiz", methods=["POST"])
@ login_required
def startQuiz():
    topicId = request.form["topicId"]
    return redirect("/study/quiz/{}".format(topicId))


@ app.route("/study/quiz/<string:topicId>", methods=["GET", "POST"])
@ login_required
def quiz(topicId):
    # Get topic name
    topicName = Topics.query.get(topicId)
    userId = session["user_id"]
    if request.method == "GET":
        vocab_schema = VocabularySchema(many=True)
        # Get all words from DB by filter
        vocabWords = Vocabularys.query.filter(and_(
            Vocabularys.user_id == userId, Vocabularys.topic_id == topicId)).all()
        jsonVocabsWord = vocab_schema.dump(vocabWords)
        # Check if User had word or phrases in DB
        if len(jsonVocabsWord) == 0:
            flash("No words or Phrases for quiz. First add some")
            return redirect("/study/{}".format(topicId))
        elif (len(jsonVocabsWord) < 4):
            flash("No enough words or Phrases for quiz. First add more, at list 4")
            return redirect("/study/{}".format(topicId))
        # Ckeck user progress
        progress_schema = ProgressSchema(many=True)
        userProgress = Progress.query.filter(and_(
            Progress.user_id == userId, Progress.topic_id == topicId)).all()
        jsonUserProgress = progress_schema.dump(userProgress)
        # Init view object
        quizObj = {}
        if len(jsonUserProgress) != 0:
            # If user have some progress in current quiz get next quiz with Low attempt and success
            randomObj = jsonVocabsWord[random.randint(
                0, len(jsonVocabsWord)-1)]
            # Check if the word in Progress db
            checkIfObjInOrigress = Progress.query.filter_by(
                vocabulary_id=randomObj["id"]).first()

            if checkIfObjInOrigress != None:
                # Already in  db
                quizObj["question"] = randomObj["origin"]
                quizObj["tryId"] = randomObj["id"]
                quizObj["answers"] = [randomObj["translate"]]
                while len(quizObj["answers"]) < 4:
                    randomAnswer = jsonVocabsWord[random.randint(
                        0, len(jsonVocabsWord)-1)]
                    if randomAnswer["id"] != quizObj["tryId"] and randomAnswer["translate"] not in quizObj["answers"]:
                        quizObj["answers"].append(randomAnswer["translate"])
                return render_template("topic_quiz.html", topic_id=topicId, topic_name=topicName.topic, quiz_Obj=quizObj)
            else:
                # NOT IN DB
                quizObj["question"] = randomObj["origin"]
                quizObj["tryId"] = randomObj["id"]
                quizObj["answers"] = [randomObj["translate"]]
                while len(quizObj["answers"]) < 4:
                    randomAnswer = jsonVocabsWord[random.randint(
                        0, len(jsonVocabsWord)-1)]
                    if randomAnswer["id"] != quizObj["tryId"] and randomAnswer["translate"] not in quizObj["answers"]:
                        quizObj["answers"].append(randomAnswer["translate"])
                return render_template("topic_quiz.html", topic_id=topicId, topic_name=topicName.topic, quiz_Obj=quizObj)
        else:
            # Get random vocabulary for first quiz in topic
            randomObj = jsonVocabsWord[random.randint(
                0, len(jsonVocabsWord)-1)]
            quizObj["question"] = randomObj["origin"]
            quizObj["tryId"] = randomObj["id"]
            quizObj["answers"] = [randomObj["translate"]]
            while len(quizObj["answers"]) < 4:
                randomAnswer = jsonVocabsWord[random.randint(
                    0, len(jsonVocabsWord)-1)]
                if randomAnswer["id"] != quizObj["tryId"] and randomAnswer["translate"] not in quizObj["answers"]:
                    quizObj["answers"].append(randomAnswer["translate"])
        return render_template("topic_quiz.html", topic_id=topicId, topic_name=topicName.topic, quiz_Obj=quizObj)
    else:
        # POST
        userAnswer = request.form.get("answer")
        tryId = request.form.get("tryId")
        if userAnswer == None:
            flash("Please select answer")
            return redirect("/study/quiz/{}".format(topicId))
        else:
            checkWord = Vocabularys.query.get(tryId)
            checkProgress = Progress.query.filter(and_(
                Progress.user_id == userId, Progress.topic_id == topicId, Progress.vocabulary_id == tryId)).first()
            # Check if user don't have the word in progress then add one
            if checkProgress == None:
                progress = Progress(
                    user_id=userId, topic_id=topicId, vocabulary_id=tryId, attempts=0, success=0)
                db.session.add(progress)
                db.session.commit()
            # Checking answer
            if userAnswer != checkWord.translate:
                userProgress = Progress.query.filter(and_(
                    Progress.user_id == userId, Progress.topic_id == topicId, Progress.vocabulary_id == tryId)).first()
                userProgress.attempts += 1
                db.session.commit()
                flash("Previous answer was wrong. Let try another one")
                return redirect("/study/quiz/{}".format(topicId))
            else:
                userProgress = Progress.query.filter(and_(
                    Progress.user_id == userId, Progress.topic_id == topicId, Progress.vocabulary_id == tryId)).first()
                userProgress.attempts += 1
                userProgress.success += 1
                db.session.commit()
                flash("Congratulation! Previos answer was correct")
                return redirect("/study/quiz/{}".format(topicId))


@ app.route("/study/<string:topic_id>")
@ login_required
def study(topic_id):
    topicTitle = Topics.query.get(topic_id)
    userId = session["user_id"]
    vocab_schema = VocabularySchema(many=True)
    # Get all words from DB by filter
    vocabsWord = Vocabularys.query.filter(and_(
        Vocabularys.user_id == userId, Vocabularys.topic_id == topic_id, Vocabularys.type == "word")).all()
    jsonVocabsWord = vocab_schema.dump(vocabsWord)
    # Get all Phrases from DB by filter
    vocabsPhrases = Vocabularys.query.filter(and_(
        Vocabularys.user_id == userId, Vocabularys.topic_id == topic_id, Vocabularys.type == "phrase")).all()
    jsonVocabsPhrases = vocab_schema.dump(vocabsPhrases)
    # Generate obj for statiscic from DB
    temp = {
        "wordAndPhrases": [],
        "attemptsAndSuccess": []
    }
    # Get data from Vocabulary table
    temp["wordAndPhrases"].append(len(vocabsWord))
    temp["wordAndPhrases"].append(len(vocabsPhrases))
    # Get data from Progress table
    progressAttemptSchema = ProgressSchema(many=True)
    progressAttempts = Progress.query.filter(and_(
        Progress.user_id == userId, Progress.topic_id == topic_id)).all()
    jsonAttempts = progressAttemptSchema.dump(progressAttempts)
    attemptsCounter = 0
    successCounter = 0
    for element in jsonAttempts:
        attemptsCounter += element["attempts"]
        successCounter += element["success"]
    temp["attemptsAndSuccess"].append(attemptsCounter)
    temp["attemptsAndSuccess"].append(successCounter)
    topicStatistic = json.dumps(temp)
    return render_template("study.html", topicTitle=topicTitle, vocabs=jsonVocabsWord, vocabsPh=jsonVocabsPhrases, userStat=topicStatistic)


@ app.route("/study/phrase/add", methods=["POST"])
@ login_required
def addPhrase():
    # Get gata from user
    topicId = request.form["topicId"]
    originPhrase = request.form["phraseOrigin"]
    translatePhrase = request.form["phraseTranslate"]
    userId = session["user_id"]
    # Check if all fields are entered
    if not originPhrase or not translatePhrase:
        flash("Origin phrase or translate not entered. Please try again")
        return redirect("/study/{}".format(topicId))
    # Add hprase to DB
    newPH = Vocabularys(user_id=userId, topic_id=topicId,
                        type="phrase", origin=originPhrase, translate=translatePhrase)
    db.session.add(newPH)
    db.session.commit()
    flash("Phrase successfully added")
    return redirect("/study/{}".format(topicId))


@ app.route("/study/phrase/edit", methods=["POST"])
@ login_required
def editPhrase():
    # Get gata from user
    topicId = request.form["topicId"]
    phraseId = request.form["phraseId"]
    originPhrase = request.form["phraseOrigin"]
    translatePhrase = request.form["phraseTranslate"]
    userId = session["user_id"]
    # Check if all fields are entered
    if not originPhrase or not translatePhrase:
        flash("Origin phrase or translate not entered. Please try again")
        return redirect("/study/{}".format(topicId))
    # Edit word in DB
    vocabPh = Vocabularys.query.get(phraseId)
    vocabPh.origin = originPhrase
    vocabPh.translate = translatePhrase
    db.session.commit()
    flash("Phrase successfully eddited")
    return redirect("/study/{}".format(topicId))


@ app.route("/study/phrase/delete", methods=["POST"])
@ login_required
def deletePhrase():
    topicId = request.form["topicId"]
    phraseId = request.form["deleteId"]
    phraseDB = Vocabularys.query.get(phraseId)
    db.session.delete(phraseDB)
    db.session.commit()
    flash("Phrase successfully deleted")
    return redirect("/study/{}".format(topicId))


@ app.route("/study/word/add", methods=["POST"])
@ login_required
def addWord():
    # Get gata from user
    topicId = request.form["topicId"]
    originWord = request.form["wordOrigin"]
    translateWord = request.form["wordTranslate"]
    userId = session["user_id"]
    # Check if all fields are entered
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


@ app.route("/study/word/edit", methods=["POST"])
@ login_required
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


@ app.route("/study/word/delete", methods=["POST"])
@ login_required
def deleteWord():
    topicId = request.form["topicId"]
    wordId = request.form["deleteId"]
    wordDB = Vocabularys.query.get(wordId)
    db.session.delete(wordDB)
    db.session.commit()
    flash("Word successfully deleted")
    return redirect("/study/{}".format(topicId))


@ app.route("/topics")
@ login_required
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


@ app.route("/topics/add", methods=["POST"])
@ login_required
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


@ app.route("/study/topic/edit", methods=["POST"])
@ login_required
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


@ app.route("/study/topic/delete", methods=["POST"])
@ login_required
def deleteTopic():
    # Get gata from user
    topicId = request.form["topicId"]
    # Get data from DB and delete
    topicDB = Topics.query.get(topicId)
    db.session.delete(topicDB)
    db.session.commit()
    flash("Topick successfully deleted")
    return redirect("/topics")


@ app.route("/topicSearch", methods=["POST"])
@ login_required
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


@ app.route("/study/getWordById", methods=["POST"])
@ login_required
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


@ app.route("/login", methods=["GET", "POST"])
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
                session["email"] = user[0].email
                return redirect("/")
            else:
                return apology("Password not match", 400)
        else:
            return apology("Email not match", 400)
    else:
        # GET
        return render_template("login.html")


@ app.route("/register", methods=["GET", "POST"])
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
                session["email"] = newUser.email
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


@ app.route("/logout")
@ login_required
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
