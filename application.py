from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #rows = db.execute("SELECT * FROM transactions GROUP BY id HAVING id = :cur_id", cur_id=session["user_id"])
    rows = db.execute(
        "SELECT symbol, sum(shares) as shares FROM transactions WHERE id = :cur_id GROUP BY symbol", cur_id=session["user_id"])
    cash = cash = db.execute("SELECT cash FROM users WHERE id = :usr", usr=session["user_id"])
    cash = cash[0]['cash']
    added_info = {}
    total_stock = 0.0
    for row in rows:
        stock = lookup(row["symbol"])
        row["name"] = stock["name"]
        row["price"] = stock["price"]
        row["total"] = (1.0 * int(row["shares"])) * float(row["price"])
        row["price"] = usd(row["price"])
        total_stock += row["total"]
        row["total"] = usd(row["total"])
    return render_template("index.html", rows=rows, cash=usd(cash), total=usd(cash + total_stock))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("enter stock symbol")
        elif not request.form.get("shares"):
            return apology("enter number of shares")

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not lookup(symbol):
            return apology("invalid stock symbol")

        elif not shares.isdigit():
            return apology("invalid input for shares: must be integer")
        shares = int(shares)

        if shares <= 0:
            return apology("shares must be a positive integer")

        cash = db.execute("SELECT cash FROM users WHERE id = :usr", usr=session["user_id"])
        quote = lookup(symbol)
        if quote["price"] * shares > cash[0]['cash']:
            return apology("can't afford")

        db.execute("INSERT INTO 'transactions' ('id', 'symbol', 'shares', 'price') VALUES(:usr, :symbol, :share, :price)",
                   usr=session["user_id"], symbol=quote["symbol"], share=shares, price=quote["price"])
        db.execute("UPDATE users SET cash = cash - :transact WHERE id = :usr",
                   transact=quote["price"] * shares, usr=session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE id = :usr_id", usr_id=session["user_id"])
    for row in transactions:
        row["price"] = usd(row["price"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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
@app.route("/quoted")
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Ensure that the user submitted a stock symbol
        if not request.form.get("symbol"):
            return apology("must enter stock symbol", 400)

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("stock symbol invalid", 400)

        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure both passwords were submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must reenter password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        pass_hash = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=pass_hash)
        if not result:
            return apology("username already exists")

        session["user_id"] = result
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET"])
@login_required
def sell_render():
    """ helper function for sell that generates the form to work around return render_template()"""
    tickers = db.execute(
        "SELECT symbol FROM transactions GROUP BY symbol HAVING id = :cur_id", cur_id=session["user_id"])
    return render_template("sell.html", tickers=tickers)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    sell_render()
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Select a stock to sell", 400)
        symbol = request.form.get("symbol")
        entry = db.execute(
            "SELECT sum(shares) as shares FROM transactions WHERE id = :cur_id GROUP BY symbol HAVING symbol = :sym", sym=symbol, cur_id=session["user_id"])
        if len(entry) == 0:
            return apology("You don't have any more of that stock")
        elif not request.form.get("shares"):
            return apology("enter an amount of shares to sell", 400)

        amount = request.form.get("shares")
        if not amount.isdigit():
            return apology("Input must be an integer")
        amount = int(amount)
        if amount <= 0:
            return apology("Input a positive integer")
        elif amount > entry[0]["shares"]:
            return apology("You don't have enough shares to sell")

        stock = lookup(symbol)
        db.execute("UPDATE users SET cash = cash + :transaction WHERE id = :cur_id",
                   transaction=stock["price"] * (1.0 * amount), cur_id=session["user_id"])
        db.execute("INSERT INTO transactions (id, symbol, shares, price) VALUES(:cur_id, :symbol, :shares, :price)",
                   cur_id=session["user_id"], symbol=symbol, shares=-1 * amount, price=stock["price"])
        return redirect("/")
    return render_template("sell.html")


@app.route("/addcash", methods=["GET", "POST"])
def addcash():
    """ personal touch, can add any amount of cash to current user """
    if request.method == "POST":
        if not request.form.get("amount"):
            return apology("must enter amount", 400)
        amount = request.form.get("amount")
        if not amount.isdigit():
            return apology("invalid input for amount: must be numeric")
        amount = float(amount)
        if amount < 0:
            return apology("amount must be positive", 400)
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :usr",
                   amount=amount, usr=session["user_id"])
        return redirect("/")

    else:
        return render_template("addcash.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
