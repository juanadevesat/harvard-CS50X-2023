from os import path
import sqlite3
from requests import session
import random
from functools import wraps
from flask import Flask, flash, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Connect database to application
app_path = path.dirname(path.abspath(__file__))
dir_path = path.join(app_path, "RPSLS_data.db")
connect = sqlite3.connect(dir_path, check_same_thread=False)
cursor = connect.cursor()


# Blank player
GUEST_PLAYER = {"user_id": None, "name": "Guest", "wins": 0, "losses": 0, "ties": 0}    

# List of options for computer
options = ["R", "P", "S", "L", "V"]


# Dict storing locations of images
optionsimg = {"R": "static/Rock.png", "P": "static/Paper.png", \
              "S": "static/Scissors.png", "L": "static/Lizard.png", \
              "V": "static/Spock.png"}


# Decorate routes to require login.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        if request.form.get("index_button") == "register":
            return redirect("/register")
        
        elif request.form.get("index_button") == "login":
            return redirect("/login")

        else:
            session.update(GUEST_PLAYER)
            return redirect("/game")

    else:
        return render_template("index.html")       


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username!")
            pwd = request.form.get("password")
            return render_template("login.html", pwd=pwd)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password!")
            name = request.form.get("username")
            return render_template("login.html", name=name)
        
        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()
        
        # Ensure username exists
        if len(rows) != 1:
            flash("Invalid username!")
            name = request.form.get("username")
            pwd = request.form.get("password")
            return render_template("login.html", name=name, pwd=pwd)

        # Ensure password is correct
        if check_password_hash(rows[0][2], request.form.get("password")) == False:
            flash("Wrong password!")
            name = request.form.get("username")
            return render_template("login.html", name=name)
        
        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        session["name"] = rows[0][1]
        session["wins"] = rows[0][3]
        session["losses"] = rows[0][4]
        session["ties"] = rows[0][5]

        # Redirect user to account site
        return redirect("/account")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any existing user_id
    session.clear()
    session.update(GUEST_PLAYER)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            pwd = request.form.get("password")
            pwd2 = request.form.get("confirmation")    
            return render_template("register.html", pwd=pwd, pwd2=pwd2)
            
        # Ensure password was submitted in both boxes
        elif not request.form.get("password") or not request.form.get("confirmation"):
            flash("must provide password and confirmation")
            name = request.form.get("username")
            return render_template("register.html", name=name)

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("passwords do not match")
            name = request.form.get("username")
            pwd = request.form.get("password")
            return render_template("register.html", name=name, pwd=pwd)
        
        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()
        
        # Ensure username does not exists
        if len(rows) > 0:
            flash("Username unavailable")
            name = request.form.get("username")
            pwd = request.form.get("password")
            pwd2 = request.form.get("confirmation")
            return render_template("register.html", name=name, pwd=pwd, pwd2=pwd2)
        
        # Add username and password hash to database
        user = request.form.get("username")
        pw_hash = generate_password_hash(request.form.get("password"))
        cursor.execute("INSERT INTO users(username, hash, wins, losses, ties) VALUES (?, ?, 0, 0, 0)", (user, pw_hash))
        connect.commit()

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        session["name"] = rows[0][1]

        # Add moves to database
        cursor.execute("INSERT INTO moves(id, R, P, S, L, V) VALUES (?, 0, 0, 0, 0, 0)", (session["user_id"],))
        connect.commit()

        # Redirect user to account page
        return redirect("/account")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    if request.method == "POST":

        # Change username button
        if "newname" in request.form or "confname" in request.form:
            if not request.form.get("newname"):
                flash("must provide new username")
                return redirect("/account")
            
            if not request.form.get("confname"):
                flash("must provide confirmation")
                return redirect("/account")

            if request.form.get("newname") != request.form.get("confname"):
                flash("New username does not match confirmation")
                return redirect("/account")
            
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("newname"),))
            usrs = cursor.fetchall()
            
            # Ensure username does not exists
            if len(usrs) > 0:
                flash("Username unavailable")
                return redirect("/account")
            
            else:
                newname = request.form.get("newname")
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (newname, session["user_id"]))
                connect.commit()
                session["name"] = request.form.get("newname")
                return redirect("/account")
        
        # Change password button
        if "curpass" in request.form:
            if not request.form.get("curpass"):
                flash("must provide current password")
                return redirect("/account")
            
            if not request.form.get("newpass"):
                flash("must provide new password")
                return redirect("/account")
            
            if not request.form.get("confpass"):
                flash("must provide confirmation")
                return redirect("/account")

            if request.form.get("newpass") != request.form.get("confpass"):
                flash("New password does not match confirmation")
                return redirect("/account")
            
            else:
                newhash = generate_password_hash(request.form.get("newpass"))
                cursor.execute("UPDATE users SET hash = ? WHERE id = ?", (newhash, session["user_id"]))
                connect.commit()

            return redirect("/account")

    else:
        # Pie chart of moves
        cursor.execute("SELECT R, P, S, L, V FROM moves WHERE id = ?", (session["user_id"],))
        movesdata = cursor.fetchall()
        moves = {"R": movesdata[0][0], "P": movesdata[0][1], "S": movesdata[0][2], "L": movesdata[0][3], "V": movesdata[0][4]}

        # Table contents for ranking
        cursor.execute("SELECT username, wins, ties, losses FROM users")
        players = cursor.fetchall()
        player_dicts = []
        for player in players:
            total = player[1] + player[2] + player[3]
            if total != 0:
                score = int((((player[2] / 2) + player[1]) / total) * 100000) + (int(total) * 5000)
            else:
                score = 0
            player_dicts.append({"score": score, "username": player[0], "wins": player[1], "ties": player[2], "losses": player[3], "total": total})

        # Sort ranking by score:
        ranking = sorted(player_dicts, key=lambda d: d['score'], reverse=True)

        for i in range(len(ranking)):
            ranking[i]["rank"] = i + 1

        return render_template("account.html", moves=moves, ranking=ranking)


@app.route("/rules", methods=["GET", "POST"])
def rules():
    if request.method == "POST":
        redirect("/")
    else:
        return render_template("rules.html")


@app.route("/game", methods=["GET", "POST"])
def game():

    playername = session["name"]
    won = session["wins"]
    lost = session["losses"]

    if request.method == "POST":
        
        playerchoice = request.form.get("game")
        computerchoice = options[random.randrange(0, 5)]
        winner = ""

        # Update choice counter in moves table:
        if session.get("user_id") is not None:
            if playerchoice == "R":
                cursor.execute("UPDATE moves SET R = R + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()
            elif playerchoice == "P":
                cursor.execute("UPDATE moves SET P = P + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()
            elif playerchoice == "S":
                cursor.execute("UPDATE moves SET S = S + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()
            elif playerchoice == "L":
                cursor.execute("UPDATE moves SET L = L + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()
            elif playerchoice == "V":
                cursor.execute("UPDATE moves SET V = V + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()
        
        if playerchoice == computerchoice:
            winner = "tie"
            session["ties"] += 1
            # Increase stats in database
            if session.get("user_id") is not None:
                cursor.execute("UPDATE users SET ties = ties + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()

        elif playerchoice == "S" and computerchoice == "P" or \
            playerchoice == "P" and computerchoice == "R" or\
            playerchoice == "R" and computerchoice == "L" or\
            playerchoice == "L" and computerchoice == "V" or\
            playerchoice == "V" and computerchoice == "S" or\
            playerchoice == "S" and computerchoice == "L" or\
            playerchoice == "L" and computerchoice == "P" or\
            playerchoice == "P" and computerchoice == "V" or\
            playerchoice == "V" and computerchoice == "R" or\
            playerchoice == "R" and computerchoice == "S":
            winner = session["name"]
            session["wins"] += 1
            # Increase stats in database
            if session.get("user_id") is not None:
                cursor.execute("UPDATE users SET wins = wins + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()
        else:
            winner = "rival"
            session["losses"] += 1
            # Increase stats in database
            if session.get("user_id") is not None:
                cursor.execute("UPDATE users SET losses = losses + 1 WHERE id = ?", (session["user_id"],))
                connect.commit()

        playerimg = optionsimg[playerchoice]
        computerimg = optionsimg[computerchoice]

        won = session["wins"]
        lost = session["losses"]

        return render_template("winner.html", playername=playername, won=won, \
                               lost=lost, playerimg=playerimg,  \
                               computerimg=computerimg, winner=winner)
        
    else:
        return render_template("game.html", playername=playername, won=won, lost=lost)


@app.route("/restart", methods=["GET", "POST"])
def restart():

    # Return scores to 0
    session["wins"], session["losses"], session["ties"] = 0, 0, 0

    # Redirect to player's choice
    if request.method == "POST":
        if request.form.get("restart") == "Yes":
            return redirect("/logout")
        elif request.form.get("restart") == "No":
            return redirect("/game")
    
    else:
        return render_template("restart.html")


@app.route("/end", methods=["GET", "POST"])
def end():
    # Declare winner and ask to restart 

    playername = session["name"]
    won = session["wins"]
    lost = session["losses"]
    
    if request.method == "POST":
        session["wins"], session["losses"] = 0, 0
        if request.form.get("restart") == "Change player":
            return redirect("/logout")
        elif request.form.get("restart") == "Go again":
            return redirect("/game")

    else:
        return render_template("endgame.html", playername=playername, \
                                won=won, lost=lost)

if __name__ == "__main__":
    app.run(port=5010, debug=False)
