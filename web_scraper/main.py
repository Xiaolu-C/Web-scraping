from multiprocessing import connection
from flask import Flask, render_template, session, redirect, request, session
import sqlite3
from flask_session import Session
# from web_scraper.others import login_required
from werkzeug.security import check_password_hash, generate_password_hash
# import logging
from functools import wraps
from scraper import check_price


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 



connection2 = sqlite3.connect(':memory:')
connection2.set_trace_callback(print)


conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()





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
    

@app.route("/", methods=["GET", "POST"])
@login_required
def home():

    user_id = session["user_id"]

    #增加产品
    if request.method == "POST":
        website = request.form.get("website")
        check_price(URL=website, user_id=user_id)
        return redirect("/")
        

    #将数据库的东西拿出来
    

    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    with connection:
        products = cursor.execute("SELECT * FROM products WHERE User_id=(?)", (user_id,))
        
    products = products.fetchall()
    #print(products)
        

    return render_template("home.html", products=products)

  




@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"

        # Query database for username

        name = request.form.get("username")
        print('lalala')
        with conn:
            rows = cursor.execute("SELECT * FROM users WHERE Username = ?", (name,))
        print('lalala')
        
        user_lst = rows.fetchall()
        
        # Ensure username exists and password is correct
        if user_lst == [] or not check_password_hash(user_lst[0][2], request.form.get("password")):
            return "invalid username and/or password"

        # Remember which user has logged in
        session["user_id"] = user_lst[0][0]

        # Redirect user to home page
        return redirect("/")
    
    else:
        return render_template("login.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # logging.info(request.form.get("username"))

        

        # 没有username
        if not request.form.get("username"):
            return "must provide username"

        # 没有password
        if not request.form.get("password"):
            return "must provide password"

        # 两次password不一样
        if not request.form.get("password")==request.form.get("confirmation"):
            return "passwords aren't matching"

        name = request.form.get("username")
        # print(name)
        # 已经存在有这个username
        with conn:
            rows = cursor.execute("SELECT * FROM users WHERE Username = (?)", (name,))
        # print("lalala")
        # print(rows.fetchall())
        if rows.fetchall() != []:
            return "invalid username and/or password"


        else:
            username = request.form.get("username")
            password = request.form.get("password")
            password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            cursor.execute("INSERT INTO users(username, hash) VALUES(?, ?)", (username, password))

            return redirect("/login")

    else:
        return render_template("register.html")





if __name__=="__main__":
    app.run()