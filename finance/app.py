import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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


db.execute("CREATE TABLE IF NOT EXISTS transactions (user_id INTEGER, symbol TEXT, shares INTEGER, price REAL, transacted DATETIME DEFAULT CURRENT_TIMESTAMP)")
db.execute("CREATE TABLE IF NOT EXISTS transactions_history (t_type TEXT, user_id INTEGER, symbol TEXT, shares INTEGER, price REAL, transacted DATETIME DEFAULT CURRENT_TIMESTAMP)")


@app.route("/")
@login_required
def index():
    # index function

    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) != 0 ", session["user_id"])
    for row in rows:
        stock_info = lookup(row["symbol"])
        row["price"] = stock_info["price"]
        row["total_value"] = row["total_shares"] * row["price"]
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    return render_template("index.html", stocks=rows, cash=cash[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # buying function

    if request.method == "GET":
        return render_template("buy.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("Symbol required", 400)
        elif lookup(symbol) == None:
            return apology("Symbol does not exist", 400)
        if not shares.isdigit():
            return apology("Shares must be positive number", 400)
        if int(shares) <= 0:
            return apology("Number of shares must be positive", 400)
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]
        int_shares = int(shares)
        if lookup(symbol)["price"] * int_shares > cash:
            return apology("You don't have enough money for this purchase", 400)

        price = lookup(symbol)["price"] * int_shares
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, int_shares, price)

        db.execute("INSERT INTO transactions_history (t_type, user_id, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
                   "bought", session["user_id"], symbol, int_shares, price)

        new_cash_value = cash - price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_value, session["user_id"])
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT symbol, shares, price, transacted, t_type FROM transactions_history WHERE user_id = ?", session["user_id"])
    for row in rows:
        stock_info = lookup(row["symbol"])
        row["price"] = stock_info["price"]
    return render_template("history.html", stocks=rows)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    # quote function

    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        stock_info = lookup(symbol)
        if stock_info is None:
            return apology("Invalid symbol", 400)
        else:
            return render_template("quoted.html", stock=stock_info)


@app.route("/register", methods=["GET", "POST"])
def register():
    """New user can register"""

    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or not username:
            return apology("Password, confirmation and name required", 400)
        elif password != confirmation:
            return apology("Password and confirmation did not match", 400)
        if not username:
            # username is blank
            return apology("Username required", 400)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) > 0:
                return apology("Username already exists", 400)
        hash = generate_password_hash(password)
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        session["user_id"] = new_user_id
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # selling function
    if request.method == "GET":
        rows = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", stocks=rows)
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        if request.form.get("symbol") == None:
            return apology("Symbol of stock required", 400)
        count = db.execute("SELECT COUNT(*) FROM transactions WHERE user_id = ? AND symbol = ?",
                           session["user_id"], request.form.get("symbol"))
        if count[0]["COUNT(*)"] == 0:
            return apology("You have no such stock", 400)
        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("Shares must be positive number", 400)
        shares = int(shares)
        if shares <= 0:
            return apology("Shares must be positive number", 400)

        shares_in_symbol = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        total_shares = shares_in_symbol[0]['SUM(shares)']
        if total_shares - shares < 0:
            return apology("You don't have enough shares", 400)

        shares_in_symbol = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE symbol = ?", request.form.get("symbol"))

        price = lookup(symbol)["price"] * shares

        db.execute("INSERT INTO transactions_history (t_type, user_id, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
                   "Sold", session["user_id"], symbol, shares, lookup(symbol)["price"] * shares)

        if total_shares - shares == 0:
            db.execute("DELETE FROM transactions WHERE symbol = ?", symbol)
        else:
            s = total_shares - shares
            db.execute("UPDATE transactions SET shares = ? WHERE symbol = ?",
                       s, request.form.get("symbol"))

        stock_info = lookup(symbol)
        share_price = stock_info["price"]
        add = share_price*shares
        cash = db.execute("SELECT cash FROM users WHERE id = ?",
                          session["user_id"])[0]["cash"] + add
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        return redirect("/")
