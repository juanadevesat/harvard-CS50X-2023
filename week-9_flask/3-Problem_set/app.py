import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    price, total, value = 0, 0, 0
    portfolio = db.execute(
        "SELECT symbol, SUM(ammount) AS ammount FROM transactions JOIN operations ON transactions.id = operations.transaction_id WHERE user_id = ? GROUP BY symbol", session["user_id"])
    for i in range(len(portfolio)):
        price = lookup(portfolio[i]["symbol"])["price"]
        value = float(price) * float(portfolio[i]["ammount"])
        portfolio[i].update({"price": usd(price), "value": usd(value)})
        total += value
    balance = float(db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    total += balance
    return render_template("index.html", balance=balance, portfolio=portfolio, price=price, value=value, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Collect data
        data = lookup(request.form.get("symbol"))
        try:
            ammount = int(request.form.get("shares"))
        except ValueError:
            return apology("Number of shares must be\na positive amount", 400)
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure symbol exists
        elif not data:
            return apology("Invalid stock symbol", 400)

        # Ensure positive number of shares was submitted
        elif not request.form.get("shares") or ammount <= 0 or ammount % 1 != 0:
            return apology("Number of shares must be\na positive amount", 400)

        else:
            # check if enough cash
            if float(data["price"]) * ammount > balance:
                return apology("Not enough funds", 400)

            else:
                # Add sale to transaction table
                db.execute("INSERT INTO transactions (symbol, price, ammount, date_time) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                            data["symbol"], usd(data["price"]), ammount)

                # Link transaction to user in operations table
                transactionid = int(db.execute("SELECT id FROM transactions ORDER BY id DESC LIMIT 1")[0]["id"])
                userid = int(session["user_id"])
                db.execute("INSERT INTO operations (user_id, transaction_id) VALUES (?, ?)", userid, transactionid)

                # Subtract cost from balance in users table
                balance -= float(data["price"]) * ammount
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

            # Redirect to homepage
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute(
        "SELECT symbol, ammount, price, date_time FROM transactions JOIN operations ON transactions.id = transaction_id WHERE user_id = ?", session["user_id"])


    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        data = lookup(request.form.get("symbol"))
        if not request.form.get("symbol") or not data:
            return apology("must provide valid symbol", 400)

        return render_template("quoted.html", data=data)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    price = 0
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted in both boxes
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exists
        if len(rows) > 0:
            return apology("Username unavailable", 400)

        # Add username and password hash to database
        user = request.form.get("username")
        pw_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", user, pw_hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    owned = db.execute("SELECT symbol, SUM(ammount) AS ammount FROM transactions JOIN operations ON transactions.id = operations.transaction_id WHERE user_id = ? GROUP BY symbol", session["user_id"])
    if request.method == "POST":

        # Collect data
        data = lookup(request.form.get("symbol"))
        ammount = int(request.form.get("shares"))
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure positive number of shares was submitted
        elif not request.form.get("shares") or ammount <= 0:
            return apology("Number of shares must be\na positive amount", 400)

        else:
            # check if enough shares
            if ammount > int(owned[0]["ammount"]):
                return apology("Not enough shares", 400)

            else:
                # Add sale to transaction table
                db.execute("INSERT INTO transactions (symbol, price, ammount, date_time) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                            data["symbol"], usd(data["price"]), -ammount)

                # Link transaction to user in operations table
                transactionid = int(db.execute("SELECT id FROM transactions ORDER BY id DESC LIMIT 1")[0]["id"])
                userid = int(session["user_id"])
                db.execute("INSERT INTO operations (user_id, transaction_id) VALUES (?, ?)", userid, transactionid)

                # Subtract cost from balance in users table
                balance += float(data["price"]) * ammount
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

            # Redirect to homepage
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", owned=owned)


@app.route("/account")
@login_required
def account():
    balance = usd(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("account.html", username=username, balance=balance)


@app.route("/account-funds", methods=["POST"])
@login_required
def funds():
    # Collect data
    balance = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    op = int(request.form.get("funds-operation"))
    try:
        ammount = int(request.form.get("funds-ammount"))
    except ValueError:
        return apology("Ammount must be a number", 400)
    new_balance = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]) + (ammount * op)

    # Verify data
    if op != 1 and op != -1:
        return apology("An error occured", 400)

    elif not request.form.get("funds-ammount") or ammount <= 0:
        return apology("Ammount must be\na positive number", 400)

    elif op == -1 and balance < ammount:
        return apology("Not enough funds", 400)

    else:
        # Update balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])
        flash("Balance updated!")
        return redirect("/account")


@app.route("/account-username", methods=["POST"])
@login_required
def new_username():
    # Ensure new username was submitted
    if not request.form.get("new-username"):
        return apology("must provide a new username", 400)
    # Ensure username does not exists
    if len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("new-username"))) > 0:
        return apology("Username unavailable", 400)

    db.execute("UPDATE users SET username = ? WHERE id = ?", request.form.get("new-username"), session["user_id"])
    flash("Username updated!")
    return redirect("/account")


@app.route("/account-password", methods=["POST"])
@login_required
def new_password():
    # Ensure password was submitted in all boxes
    if not request.form.get("old-password"):
        return apology("must provide current password", 400)

    elif not request.form.get("new-password") or not request.form.get("confirm-new-password"):
        return apology("must provide new password", 400)

    elif request.form.get("new-password") != request.form.get("confirm-new-password"):
        return apology("new passwords do not match", 400)

    elif not check_password_hash(db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["hash"], request.form.get("old-password")):
        return apology("current password is incorrect", 400)

    else:
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
            request.form.get("new-password")), session["user_id"])
        flash("Password updated!")
        return redirect("/account")